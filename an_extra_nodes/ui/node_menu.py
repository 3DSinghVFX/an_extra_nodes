import bpy
from animation_nodes.ui.node_menu import insertNode

class ExtensionMenu(bpy.types.Menu):
    bl_idname = "AN_MT_extension_menu"
    bl_label = "Extra Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "an_MaterialInstancerNode", "Material Instancer")

def drawMenu(self, context):
    if context.space_data.tree_type != "an_AnimationNodeTree": return

    layout = self.layout
    layout.operator_context = "INVOKE_DEFAULT"

    layout.separator()
    layout.menu("AN_MT_extension_menu", text = "Extra Menu", icon = "SCRIPTPLUGINS")

def register():
    bpy.types.NODE_MT_add.append(drawMenu)

def unregister():
    bpy.types.NODE_MT_add.remove(drawMenu)
