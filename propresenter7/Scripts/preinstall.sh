#!/bin/bash

# preinstall.sh
# Marc Thielemann, 2019/09/15
# David Tilley, 2020/12/30

# redirect all output to /dev/null
exec >/dev/null 2>&1

helperPlistPath="$3/Library/LaunchDaemons/com.renewedvision.InstallHelper.plist"

/usr/bin/killall Privileges

# unload the launchd plist only if installing on the boot volume
if [[ "$3" = "/" ]]; then
	/bin/launchctl bootout system "$helperPlistPath"
fi

/bin/rm -rf "$helperPlistPath" \
            "$3/Library/PrivilegedHelperTools/com.renewedvision.InstallHelper" \
            "$3/Applications/ProPresenter.app"

exit 0