import pytest

from aspose_psd_foss.coreexceptions.notsupportedexception import NotSupportedException
from aspose_psd_foss.layers.blendmode import BlendMode
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase
from aspose_psd_foss.image import Image
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.layers.layer import Layer
from aspose_psd_foss.layers.channelinformation import ChannelInformation
from aspose_psd_foss.layers.layerblendingrangesdata import LayerBlendingRangesData
from aspose_psd_foss.layers.layerresource import LayerResource
from aspose_psd_foss.layers.globallayermaskinfo import GlobalLayerMaskInfo

from aspose_psd_foss.rectangle import Rectangle
from aspose_psd_foss.point import Point
from aspose_psd_foss.size import Size
from aspose_psd_foss.resourceblock import ResourceBlock
from aspose_psd_foss.colormodes import ColorModes



class TestAsposeCompatibility(PsdTestFixtureBase):
    def test_image_load_official_returns_psd(self):
        with Image.load(self.get_test_data_path("test.psd")) as image:
            psd_image = image  # Image.load returns a PsdImage instance
            assert psd_image.width == 100
            assert psd_image.channels_count == 3
            assert len(psd_image.layers) == 2

    def test_metadata_officialtypes_reads(self):
        with Image.load(self.get_test_data_path("test.psd")) as img:
            psd_image = img
            layer = psd_image.layers[0]

            bounds = layer.bounds
            blend_mode_key = layer.blend_mode_key

            assert bounds == Rectangle(0, 0, 100, 100)
            assert blend_mode_key == BlendMode.NORMAL
            assert layer.opacity == 255
            assert layer.is_visible is True

    def test_channels_officialshape_readsonly(self):
        with Image.load(self.get_test_data_path("test.psd")) as img:
            psd_image = img
            layer = psd_image.layers[0]

            channel_information = layer.channel_information

            assert layer.channels_count == len(channel_information)
            assert channel_information
            assert channel_information[0].length > 0
            with pytest.raises(NotSupportedException):
                layer.channel_information = channel_information

    def test_layermask_officialshape_reads(self):
        with Image.load(self.get_test_data_path("test.psd")) as img:
            psd_image = img
            layer = psd_image.layers[0]

            assert layer.layer_mask_data is None
            assert layer.layer_blending_ranges_data.length == 40
            with pytest.raises(NotSupportedException):
                layer.layer_mask_data = None
            with pytest.raises(NotSupportedException):
                layer.layer_blending_ranges_data = LayerBlendingRangesData()

    def test_rectangle_mutableshape_updates(self):
        rectangle = Rectangle(Point(10, 20), Size(30, 40))

        rectangle.location = Point(15, 25)
        rectangle.size = Size(35, 45)
        rectangle.right = 60
        rectangle.bottom = 80

        assert rectangle.x == 15
        assert rectangle.y == 25
        assert rectangle.width == 45
        assert rectangle.height == 55
        assert rectangle.contains(Point(30, 40)) is True
        assert rectangle.intersects_with(
            Rectangle.from_left_top_right_bottom(50, 70, 70, 90)
        ) is True

        rectangle.offset(Point(5, -5))
        rectangle.inflate(Size(1, 2))

        assert rectangle == Rectangle.from_left_top_right_bottom(19, 18, 66, 77)

    def test_image_setters_updatemetadata(self):
        with Image.load(self.get_test_data_path("test.psd")) as img:
            psd_image = img
            layers = psd_image.layers
            version = psd_image.version

            psd_image.color_mode = ColorModes.RGB
            psd_image.layers = layers
            psd_image.global_angle = 45
            psd_image.version = version

            assert psd_image.color_mode == ColorModes.RGB
            assert len(psd_image.layers) == len(layers)
            assert psd_image.global_angle == 45
            assert psd_image.version == version

    def test_resources_officialshape_reads(self):
        with Image.load(self.get_test_data_path("test.psd")) as img:
            psd_image = img

            image_resources = psd_image.image_resources
            global_layer_resources = psd_image.global_layer_resources
            global_layer_mask_info = psd_image.global_layer_mask_info
            active_layer = psd_image.active_layer

            assert psd_image.size == Size(psd_image.width, psd_image.height)
            assert image_resources
            assert image_resources[0].id != 0
            assert image_resources[0].data_size >= 0
            assert not global_layer_resources
            assert global_layer_mask_info is not None
            assert active_layer is psd_image.layers[0]
            assert psd_image.is_flatten is False
            assert psd_image.has_transparency_data is False

            with pytest.raises(NotSupportedException):
                psd_image.image_resources = image_resources
            with pytest.raises(NotSupportedException):
                psd_image.global_layer_resources = global_layer_resources
            with pytest.raises(NotSupportedException):
                psd_image.active_layer = active_layer
            with pytest.raises(NotSupportedException):
                psd_image.has_transparency_data = True

    def test_save_officialmutation_persists(self):
        output_file = self.get_persistent_artifact_path(
            "official_style_layer_mutation.psd"
        )

        with Image.load(self.get_test_data_path("test.psd")) as img:
            psd_image = img
            layer = psd_image.layers[0]
            layer.name = "Official style"
            layer.left = 10
            layer.top = 20
            layer.right = 40
            layer.bottom = 60
            layer.blend_mode_key = BlendMode.MULTIPLY
            psd_image.save(output_file)

        with Image.load(output_file) as reloaded_img:
            reloaded = reloaded_img
            layer = reloaded.layers[0]
            assert layer.name == "Official style"
            assert layer.bounds == Rectangle(0, 0, 30, 40)
            assert layer.left == 10
            assert layer.top == 20
            assert layer.right == 40
            assert layer.bottom == 60
            assert layer.blend_mode_key == BlendMode.MULTIPLY
