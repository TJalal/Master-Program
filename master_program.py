import os
from appJar import gui

__version__ = "0.1"

def update(dl_url, force_update=False):
    """
Attempts to download the update url in order to find if an update is needed.
If an update is needed, the current script is backed up and the update is
saved in its place.
"""
    import urllib
    import re
    from subprocess import call
    def compare_versions(vA, vB):
        """
Compares two version number strings
@param vA: first version string to compare
@param vB: second version string to compare
@author <a href="http_stream://sebthom.de/136-comparing-version-numbers-in-jython-pytho/">Sebastian Thomschke</a>
@return negative if vA < vB, zero if vA == vB, positive if vA > vB.
"""
        if vA == vB: return 0

        def num(s):
            if s.isdigit(): return int(s)
            return s

        seqA = map(num, re.findall('\d+|\w+', vA.replace('-SNAPSHOT', '')))
        seqB = map(num, re.findall('\d+|\w+', vB.replace('-SNAPSHOT', '')))

        # this is to ensure that 1.0 == 1.0.0 in cmp(..)
        lenA, lenB = len(seqA), len(seqB)
        for i in range(lenA, lenB): seqA += (0,)
        for i in range(lenB, lenA): seqB += (0,)

        rc = cmp(seqA, seqB)

        if rc == 0:
            if vA.endswith('-SNAPSHOT'): return -1
            if vB.endswith('-SNAPSHOT'): return 1
        return rc

    # dl the first 256 bytes and parse it for version number
    try:
        http_stream = urllib.urlopen(dl_url)
        update_file = http_stream.read(256)
        http_stream.close()
    except IOError, (errno, strerror):
        print "Unable to retrieve version data"
        print "Error %s: %s" % (errno, strerror)
        return

    match_regex = re.search(r'__version__ *= *"(\S+)"', update_file)
    if not match_regex:
        print "No version info could be found"
        return
    update_version = match_regex.group(1)

    if not update_version:
        print "Unable to parse version data"
        return

    if force_update:
        print "Forcing update, downloading version %s..." \
            % update_version
    else:
        cmp_result = compare_versions(__version__, update_version)
        if cmp_result < 0:
            print "Newer version %s available, downloading..." % update_version
        elif cmp_result > 0:
            print "Local version %s newer then available %s, not updating." \
                % (__version__, update_version)
            return
        else:
            print "You already have the latest version."
            return

    # dl, backup, and save the updated script
    app_path = os.path.realpath(sys.argv[0])

    if not os.access(app_path, os.W_OK):
        print "Cannot update -- unable to write to %s" % app_path

    dl_path = app_path + ".new"
    backup_path = app_path + ".old"
    try:
        dl_file = open(dl_path, 'w')
        http_stream = urllib.urlopen(dl_url)
        total_size = None
        bytes_so_far = 0
        chunk_size = 8192
        try:
            total_size = int(http_stream.info().getheader('Content-Length').strip())
        except:
            # The header is improper or missing Content-Length, just download
            dl_file.write(http_stream.read())

        while total_size:
            chunk = http_stream.read(chunk_size)
            dl_file.write(chunk)
            bytes_so_far += len(chunk)

            if not chunk:
                break

            percent = float(bytes_so_far) / total_size
            percent = round(percent*100, 2)
            sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" %
                (bytes_so_far, total_size, percent))

            if bytes_so_far >= total_size:
                sys.stdout.write('\n')

        http_stream.close()
        dl_file.close()
    except IOError, (errno, strerror):
        print "Download failed"
        print "Error %s: %s" % (errno, strerror)
        return

    try:
    	if os.path.isfile(backup_path):
            os.remove(backup_path)
        os.rename(app_path, backup_path)
    except OSError, (errno, strerror):
        print "Unable to rename %s to %s: (%d) %s" \
            % (app_path, backup_path, errno, strerror)
        return

    try:
        os.rename(dl_path, app_path)
    except OSError, (errno, strerror):
        print "Unable to rename %s to %s: (%d) %s" \
            % (dl_path, app_path, errno, strerror)
        return

    try:
        import shutil
        shutil.copymode(backup_path, app_path)
    except:
        os.chmod(app_path, 0755)

    print "New version installed as %s" % app_path
    print "(previous version backed up to %s)" % (backup_path)
    return


modules = ["sys",
			"pexpect"]

def import_modules(listOfModules):
	for module in listOfModules:
		try:
			print("Pip installing {}".format(module))
			os.system("pip install {} -U".format(module))
			print("Import: {} - SUCCESS".format(module))
		except ImportError:
			print("Issue pip installing {}".format(module))

#import_modules(modules)



def checkStop():
    return app.yesNoBox("Confirm Exit", "Are you sure you want to exit the application?")

def press(name):
	app.popUp("Test", "You pressed {}".format(name), "info")


def build_test_UI():
	pass
	# def launch(win):
	# 	if win == "one":
	# 		app.showSubWindow("oneWindow")
	# 		app.hide()
	# 	else:
	# 		app.showSubWindow("twoWindow")
	# 		app.hide()

	# def back_to_main(name):
	# 	app.hideSubWindow(name)
	# 	app.show()

	# app=gui()

	# # these go in the main window
	# app.addButtons(["one", "two"], launch)

	# # this is a pop-up
	# app.startSubWindow("oneWindow", modal=True)
	# app.addLabel("l1", "SubWindow One")
	# app.addNamedButton("CLOSE", "oneWindow", back_to_main)
	# app.stopSubWindow()

	# # this is another pop-up
	# app.startSubWindow("twoWindow")
	# app.addLabel("l2", "SubWindow Two")
	# app.addNamedButton("CLOSE", "twoWindow", back_to_main)
	# app.stopSubWindow()

	# app.go()

def build_main_UI():
	app.setLocation("CENTER")
	app.setBg("lightgrey")

	app.addLabel("l2", "Hello, what would you like to do?")
	app.setLabelBg("l2", "lightblue")

	with app.labelFrame("Tests", colspan=2, sticky="news", expand="both"):
		app.button("Current Response Automation", press)
		app.button("Automated Insertion Test", press)
		app.button("SICLOPS Data Analyzer", press)
		app.button("Device Monitor", press)
	 	app.button("Name Generator", press)
	app.addButtons(["Setup", "Cancel"], press)


	#app.setStopFunction(checkStop)
	#app.setFastStop(True)
	app.go()

#app = gui("USBOT {}".format(__version__))
#build_main_UI()


if __name__ == "__main__":
	update("https://stash.sd.apple.com/users/tjalal/repos/master-program/raw/master_program.py?at=refs%2Fheads%2Fmaster")
