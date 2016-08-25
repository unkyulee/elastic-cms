import os
import datetime

def save(file, allowed_exts, prefix, upload_dir):
    filename = ""
    if AllowedFile(allowed_exts, file.filename):
        # save the file splitted into year/month folder
        # in order to have limited number of files in each folder
        now = datetime.datetime.now()
        path = "{}/{}".format(now.year, now.month)
        filename = "{}/{}_{}".format(path, prefix, file.filename)
        # create dir
        upload_path = "{}/{}".format(upload_dir, path)
        if not os.path.exists(upload_path): os.makedirs(upload_path)
        # save file
        file.save(os.path.join(upload_dir, filename))
        return filename
    else:
        raise Exception(
            "Allowed file extenstions are ({})".format(allowed_exts)
        )


def AllowedFile(AllowedExts, filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in AllowedExts
