import lx
import lxu.command

import osn_to_tsn


class BlessedCommand(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def cmd_Interact(self):
        pass

    def basic_Execute(self, msg, flags):
        reload(osn_to_tsn)
        osn_to_tsn.execute(msg, flags)

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(BlessedCommand, "cs_osn_to_tsn")
