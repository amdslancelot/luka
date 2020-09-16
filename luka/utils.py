import re

def get_pname_and_else(s):
    '''
    return (<PACKAGE_NAME>, <VERSION>, <RELEASE>, <OS_VERSION>, <PLATFORM>)
    '''
    pname = None
    version = None
    release = None
    os_ver = None
    platform = None

    match = re.search(r"\-[0-9]", s)
    if not match:
        return (pname, version, release, os_ver, platform)
    pname = s[:match.start()].lower()
    rest = s[match.start()+1:]

    match = re.search(r"\-[0-9]", rest)
    if not match:
        version = rest
        return (pname, version, release, os_ver, platform)
    version = rest[:match.start()].lower()
    rest = rest[match.start()+1:]

    match = re.search(r"\.[a-zA-Z]", rest)
    if not match:
        release = rest
        return (pname, version, release, os_ver, platform)
    release = rest[:match.start()].lower()
    rest = rest[match.start()+1:]

    match = re.search(r"\.[a-zA-Z]", rest)
    if not match:
        os_ver = rest
        return (pname, version, release, os_ver, platform)
    os_ver = rest[:match.start()].lower()
    platform = rest[match.start()+1:].lower()
    if ".rpm" in platform:
        platform.replace(".rpm", "")
    if ".src.rpm" in platform:
        platform.replace(".src.rpm", "")

    return (pname, version, release, os_ver, platform)
