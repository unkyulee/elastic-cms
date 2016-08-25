import importlib
from sqlalchemy import create_engine, text
from threading import Thread
from Task.lib import *

g = None
def run(p):
    global g; g = p["g"];
    InstanceStatus = "ERROR"

    try:
        # if there some more task to run
        # TaskStatus = TaskInstance.STATUS_WAITING
        # otherwise finish the task
        # InstanceStatus = TaskInstance.STATUS_COMPLETED

        # Run Available Actions
        Actions = GetAvailableActions(
            p["DBEngine"], p["Action"].TaskId, p["TaskInstance"].id,
            p["Action"].OrderKey)

        for a in Actions:
            # Form Parameter Dictionary
            param = {
                "g": g,
                "Action": a,
                "TaskInstance": p["TaskInstance"],
                "DBEngine": p["DBEngine"],
                "log": ActionLog(
                        DBEngine=p["DBEngine"],
                        TaskId=a.TaskId,
                        TaskInstanceId=p["TaskInstance"].id,
                        ActionId=a.id)
            }
            # Set Start running flag
            param["log"].log("TAG", "Action Started", "STARTED")

            # Start Action Thread
            Thread(target = RunAction, args = (param,)).start()

        # Check if there are any actions left to run
        if IsActionsRemaining(DBEngine=p["DBEngine"],
                              TaskId=p["Action"].TaskId,
                              TaskInstanceId=p["TaskInstance"].id,
                              OrderKey=p["Action"].OrderKey):
            InstanceStatus = "WAITING"

        else:
            # Wrap up task
            exec (p["action"]['query'], globals())
            InstanceStatus = "COMPLETED"


        # Check if any action has failed
        if IsAnyActionFailed(DBEngine=p["DBEngine"],
                              TaskId=p["Action"].TaskId,
                              TaskInstanceId=p["TaskInstance"].id,
                              OrderKey=p["Action"].OrderKey):
            InstanceStatus = "ERROR"

    except Exception, e:
        p["log"].error("Task Runner Failed", e)

    # Should return "COMPLETED" only when all actions are exhausted
    # NEVER return True - because we don't want the rest of the action to be run
    return InstanceStatus


def RunAction(p):
    try:
        # Find Task Module
        t = importlib.import_module(
                "Task.TaskModule.{}".format(p["Action"].TaskModuleName))

        # Run Action
        if t.run(p) == True:
            # Set output parameter as READY
            Outputs = GetOutputParameters(p["DBEngine"], p["Action"].id)
            for o in Outputs:
                p["log"].log("OUT", "Output Ready: {}".format(o), o)

            # Set Completed flag
            p["log"].log("TAG", "Action Ended", "COMPLETED")

        else:
            # Failed
            p["log"].log("TAG", "Action Failed", "FAILED")
    except Exception, e:
        # Failed
        p["log"].error("Action failed", e)
        p["log"].log("TAG", "Action Failed", "FAILED")


# Look into the list of actions and see there are any available actions
def GetAvailableActions(DBEngine, TaskId, TaskInstanceId, OrderKey):
    SQL = """
    SELECT DISTINCT
        A.*,
        T.Name as TaskModuleName
    FROM
        Action A
    	INNER JOIN TaskModule as T ON
            T.TaskModuleId = A.TaskModuleId
    	LEFT OUTER JOIN ActionParam P ON
            P.ActionId = A.id AND Type = "IN"
    	LEFT OUTER JOIN TaskLog L ON
            L.Info = P.Parameter AND
            L.TaskInstanceId = :TaskInstanceId AND
            L.Status = "OUT"
        -- If it's already done
	    LEFT OUTER JOIN TaskLog C ON
            C.Status = "TAG" AND
            C.ActionId = A.id AND
            C.TaskInstanceId = :TaskInstanceId
    WHERE
        A.TaskId=:TaskId
        AND A.Enabled=1
        AND A.OrderKey > :OrderKey
        -- All input ready or no input
    	AND (
            -- No input
            (P.Parameter IS NULL AND L.Info IS NULL)
            OR
            (P.Parameter IS NOT NULL AND L.Info IS NOT NULL)
        )
        -- Shouldn't be completed
	    AND C.id IS NULL
        -- All input should be ready
        -- check required input count and ready input count matches
        AND
        (
            SELECT COUNT(*) FROM Action A1
            INNER JOIN ActionParam P1 ON P1.ActionId = A1.id AND P1.Type = "IN"
            WHERE A1.id = A.id
        ) = (
            SELECT COUNT(*) FROM TaskLog L2
            INNER JOIN ActionParam P2 ON P2.Parameter = L2.Info AND P2.Type = "IN"
            WHERE
                L2.Status = "OUT" AND
                L2.TaskInstanceId = :TaskInstanceId AND
                P2.ActionId = A.id
        )
    """
    ActionList = []
    with DBEngine.connect() as conn:
        results = conn.execute(text(SQL), TaskId=TaskId,
                               TaskInstanceId=TaskInstanceId, OrderKey=OrderKey)
        # exhaust the result
        for r in results: ActionList.append(r)
    return ActionList

# Is Error?
def IsAnyActionFailed(DBEngine, TaskId, TaskInstanceId, OrderKey):
    ActionFailed = False

    SQL = """
    SELECT
        A.id
    FROM
        Action as A
        -- if any action has FAILED tag then it's entire task should end
        INNER JOIN TaskLog as L ON
            L.ActionId = A.id
            AND L.Info = "FAILED"
            AND L.TaskInstanceId = :TaskInstanceId
    WHERE
        A.TaskId=:TaskId AND A.Enabled=1 AND A.OrderKey > :OrderKey
    """

    with DBEngine.connect() as conn:
        results = conn.execute(text(SQL),
                               TaskId=TaskId,
                               TaskInstanceId=TaskInstanceId,
                               OrderKey=OrderKey)
        for r in results:
            ActionFailed = True

    return ActionFailed


# Any actions left?
def IsActionsRemaining(DBEngine, TaskId, TaskInstanceId, OrderKey):
    ActionsRemaining = False

    SQL = """
    SELECT
        A.id
    FROM
        Action as A
        -- if the action has COMPLETED tag then it's done
        LEFT OUTER JOIN TaskLog as L ON
            L.ActionId = A.id
            AND L.Info = "STARTED"
            AND L.TaskInstanceId = :TaskInstanceId
    WHERE
        A.TaskId=:TaskId AND A.Enabled=1 AND A.OrderKey > :OrderKey
        -- We are searching for if there are any actions not completed
        AND L.Info IS NULL
    """

    with DBEngine.connect() as conn:
        results = conn.execute(text(SQL),
                               TaskId=TaskId,
                               TaskInstanceId=TaskInstanceId,
                               OrderKey=OrderKey)
        for r in results:
            ActionsRemaining = True

    return ActionsRemaining


# Get Output Parameters
def GetOutputParameters(DBEngine, ActionId):
    SQL = """
    SELECT Parameter FROM ActionParam WHERE ActionId=:ActionId AND Type = "OUT"
    """

    Outputs = []
    with DBEngine.connect() as conn:
        results = conn.execute(text(SQL), ActionId=ActionId)
        for r in results:
            Outputs.append(r.Parameter)

    return Outputs
