import sys
sys.path.insert(0, r'c:\GitHub\Interzen\Interzen.POC\ZenIa\src')

print('PYTHON PATH SET')

try:
    import core.logging_utils as lu
    import mcp_client.direct_client as dc
    import mcp_client.client as mc
    import mcp_server.server as ms
    import frontend.app as fa
    print('IMPORTS_OK')
    print('Logging utils functions:', [name for name in dir(lu) if not name.startswith('_')])
except Exception as e:
    import traceback
    traceback.print_exc()
    print('IMPORT_ERROR', str(e))
