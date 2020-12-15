import bpy
from animation_nodes.ui.node_menu import insertNode

def drawMenu(self, context):
    if context.space_data.tree_type != "an_AnimationNodeTree": return

    layout = self.layout
    layout.operator_context = "INVOKE_DEFAULT"

    layout.separator()
    layout.menu("AN_MT_an_extranodes_menu", text = "Extra Nodes Menu", icon = "SCRIPTPLUGINS")

class ANExtraNodesMenu(bpy.types.Menu):
    bl_idname = "AN_MT_an_extranodes_menu"
    bl_label = "Extra Nodes Menu"

    def draw(self, context):
        layout = self.layout

        layout.menu("AN_MT_an_en_falloff_menu", text = "Falloff", icon = "SMOOTHCURVE")
        layout.separator()
        layout.menu("AN_MT_an_en_material_menu", text = "Material", icon = "NODE_MATERIAL")
        layout.separator()
        layout.menu("AN_MT_an_en_texture_menu", text = "Texture", icon = "TEXTURE_DATA")

class FalloffMenu(bpy.types.Menu):
    bl_idname = "AN_MT_an_en_falloff_menu"
    bl_label = "Falloff Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "an_TextureFalloffNode", "Texture")

class MaterialMenu(bpy.types.Menu):
    bl_idname = "AN_MT_an_en_material_menu"
    bl_label = "Material Menu"

    def draw(self, context):
        layout = self.layout
        layout.separator()
        insertNode(layout, "an_MaterialInstancerNode", "Material Instancer")

class TexturelMenu(bpy.types.Menu):
    bl_idname = "AN_MT_an_en_texture_menu"
    bl_label = "Texture Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "an_TextureInputNode", "Texture Input")

def register():
    bpy.types.NODE_MT_add.append(drawMenu)

def unregister():
    bpy.types.NODE_MT_add.remove(drawMenu)
