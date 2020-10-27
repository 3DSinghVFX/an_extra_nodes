import bpy
from animation_nodes.ui.node_menu import insertNode

def draw(self, context):
    layout = self.layout
    layout.separator()
    insertNode(layout, "an_MaterialInstancerNode", "Material Instancer")

def register():
    bpy.types.AN_MT_material_menu.append(draw)

def unregister():
    bpy.types.AN_MT_material_menu.remove(draw)
