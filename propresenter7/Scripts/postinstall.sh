#!/bin/bash

# postinstall.sh
# Marc Thielemann, 2020/01/21
# David Tiley, 2020/12/30

exitCode=0

helperPath="$3/Applications/ProPresenter.app/Contents/Library/LaunchServices/com.renewedvision.InstallHelper"

if [[ -f "$helperPath" ]]; then

	# create the target directory if needed
	if [[ ! -d "$3/Library/PrivilegedHelperTools" ]]; then
		/bin/mkdir -p "$3/Library/PrivilegedHelperTools"
		/bin/chmod 755 "$3/Library/PrivilegedHelperTools"
		/usr/sbin/chown -R root:wheel "$3/Library/PrivilegedHelperTools"
	fi
	
	# move the privileged helper into place
	/bin/cp -f "$helperPath" "$3/Library/PrivilegedHelperTools"
	
	if [[ $? -eq 0 ]]; then
		/bin/chmod 755 "$3/Library/PrivilegedHelperTools/com.renewedvision.InstallHelper"

		# create the launchd plist
		helperPlistPath="$3/Library/LaunchDaemons/com.renewedvision.InstallHelper.plist"
	
		/bin/cat > "$helperPlistPath" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD helperPlistPath 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>com.renewedvision.InstallHelper</string>
	<key>MachServices</key>
	<dict>
		<key>com.renewedvision.InstallHelper</key>
		<true/>
	</dict>
	<key>ProgramArguments</key>
	<array>
		<string>/Library/PrivilegedHelperTools/com.renewedvision.InstallHelper</string>
	</array>
</dict>
</plist>
EOF

		/bin/chmod 644 "$helperPlistPath"
		
		# load the launchd plist only if installing on the boot volume
		if [[ "$3" = "/" ]]; then
			/bin/launchctl bootstrap system "$helperPlistPath"
		fi
		
		# restart the Dock if Privileges is in there. This ensures proper loading
		# of the (updated) Dock tile plug-in
		
		# get the currently logged-in user and go ahead if it's not root
		currentUser=$(/bin/ls -l /dev/console | /usr/bin/awk '{ print $3 }')

		if [[ -n "$currentUser" && "$currentUser" != "root" ]]; then
			if [[ -n $(/usr/bin/sudo -u "$currentUser" /usr/bin/defaults read com.apple.dock "persistent-apps" | /usr/bin/grep "/Applications/ProPresenter.app") ]]; then
				/usr/bin/killall Dock
			fi
		fi

	else
		exitCode=1
	fi
else
	exitCode=1
fi

exit $exitCode