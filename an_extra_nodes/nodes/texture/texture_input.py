import bpy
from . c_utils import getTextureColors
from animation_nodes.base_types import AnimationNode, VectorizedSocket
from animation_nodes.data_structures import DoubleList, Color, ColorList

class TextureInputNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_TextureInputNode"
    bl_label = "Texture Input"

    useVectorList: VectorizedSocket.newProperty()

    def create(self):
        self.newInput("Texture", "Texture", "texture", defaultDrawType = "PROPERTY_ONLY")
        self.newInput(VectorizedSocket("Vector", "useVectorList",
            ("Location", "location"), ("Locations", "locations")))
        self.newInput("Matrix", "Transformation", "transformation", hide = True)
        self.newInput("Scene", "Scene", "scene", hide = True)

        self.newOutput(VectorizedSocket("Color", "useVectorList",
            ("Color", "color"), ("Colors", "colors")))
        self.newOutput(VectorizedSocket("Float", "useVectorList",
            ("Red", "red"), ("Reds", "reds")))
        self.newOutput(VectorizedSocket("Float", "useVectorList",
            ("Green", "green"), ("Greens", "greens")))
        self.newOutput(VectorizedSocket("Float", "useVectorList",
            ("Blue", "blue"), ("Blues", "blues")))
        self.newOutput(VectorizedSocket("Float", "useVectorList",
            ("Alpha", "alpha"), ("Alphas", "alphas")))
        self.newOutput(VectorizedSocket("Float", "useVectorList",
            ("Intensity", "intensity"), ("Intensities", "intensities")))

        visibleOutputs = ("Color", "Colors")
        for socket in self.outputs:
            socket.hide = socket.name not in visibleOutputs

    def drawAdvanced(self, layout):
        box = layout.box()
        col = box.column(align = True)
        col.label(text = "Info", icon = "INFO")
        col.label(text = "For External Texture, Alpha = Alpha")
        col.label(text = "For Internal Texture, Alpha = Intensity")

    def getExecutionFunctionName(self):
        if self.useVectorList:
            return "executeList"
        else:
            return "executeSingle"

    def executeSingle(self, texture, location, matrix, scene):
        if texture is None:
            return Color((0, 0, 0, 0)), 0, 0, 0, 0, 0

        if texture.type == "IMAGE":
            if texture.image is not None and texture.image.source in ["SEQUENCE", "MOVIE"]:
                texture.image_user.frame_current = scene.frame_current

        color = Color(texture.evaluate(matrix @ location))
        r = color.r
        g = color.g
        b = color.b
        return color, color.r, color.g, color.b, color.a, (r + g + b) / 3

    def executeList(self, texture, locations, matrix, scene):
        if texture is None or len(locations) == 0:
            return ColorList(), DoubleList(), DoubleList(), DoubleList(), DoubleList(), DoubleList()

        if texture.type == "IMAGE":
            if texture.image is not None and texture.image.source in ["SEQUENCE", "MOVIE"]:
                texture.image_user.frame_current = scene.frame_current

        return getTextureColors(texture, locations, matrix)
