import pytest
from aspose_psd_foss.image import Image
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.layers.layer import Layer
from aspose_psd_foss.layers.blendmode import BlendMode
from aspose_psd_foss.layers.layerblendingrangesdata import LayerBlendingRangesData
from aspose_psd_foss.layers.channelinformation import ChannelInformation
from aspose_psd_foss.rectangle import Rectangle
from aspose_psd_foss.point import Point
from aspose_psd_foss.size import Size
from aspose_psd_foss.resourceblock import ResourceBlock
from aspose_psd_foss.layers.globallayermaskinfo import GlobalLayerMaskInfo
from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase


class TestAsposeCompatibility(PsdTestFixtureBase):
    def test_image_load_official_returns_psd(self):
        with Image.load(self.get_test_data_path("test.psd")) as image:
            psd_image = image.as_psd()

            assert psd_image.width == 100
            assert psd_image.channels_count == 3
            assert len(psd_image.layers) == 2

    def test_metadata_official_types_reads(self):
        with PsdImage.load(self.get_test_data_path("test.psd")) as image:
            layer = image.layers[0]

            bounds = layer.bounds
            blend_mode_key = layer.blend_mode_key

            assert bounds == Rectangle(0, 0, 100, 100)
            assert blend_mode_key == BlendMode.Normal
            assert layer.opacity == 255
            assert layer.is_visible is True

    def test_channels_official_shape_reads_only(self):
        with PsdImage.load(self.get_test_data_path("test.psd")) as image:
            layer = image.layers[0]

            channel_information = layer.channel_information

            assert layer.channels_count == len(channel_information)
            assert len(channel_information) > 0
            assert channel_information[0].length > 0
            with pytest.raises(NotImplementedError):
                layer.channel_information = channel_information

    def test_layer_mask_official_shape_reads(self):
        with PsdImage.load(self.get_test_data_path("test.psd")) as image:
            layer = image.layers[0]

            assert layer.layer_mask_data is None
            assert len(layer.layer_blending_ranges_data) == 40
            with pytest.raises(NotImplementedError):
                layer.layer_mask_data = None
            with pytest.raises(NotImplementedError):
                layer.layer_blending_ranges_data = LayerBlendingRangesData()

    def test_rectangle_mutable_shape_updates(self):
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
        assert rectangle.intersectsWith(Rectangle.from_left_top_right_bottom(50, 70, 70, 90)) is True

        rectangle.offset(Point(5, -5))
        rectangle.inflate(Size(1, 2))

        assert rectangle == Rectangle.from_left_top_right_bottom(19, 18, 66, 77)

    def test_image_setters_update_metadata(self):
        with PsdImage.load(self.get_test_data_path("test.psd")) as image:
            layers = image.layers
            version = image.version

            image.color_mode = ColorModes.Rgb
            image.layers = layers
            image.global_angle = 45
            image.version = version

            assert image.color_mode == ColorModes.Rgb
            assert len(image.layers) == len(layers)
            assert image.global_angle == 45
            assert image.version == version

    def test_resources_official_shape_reads(self):
        with PsdImage.load(self.get_test_data_path("test.psd")) as image:
            image_resources = image.image_resources
            global_layer_resources = image.global_layer_resources
            global_layer_mask_info = image.global_layer_mask_info
            active_layer = image.active_layer

            assert image.size == Size(image.width, image.height)
            assert len(image_resources) > 0
            assert image_resources[0].id != 0
            assert image_resources[0].data_size >= 0
            assert len(global_layer_resources) == 0
            assert global_layer_mask_info is not None
            assert active_layer is image.layers[0]
            assert image.is_flatten is False
            assert image.has_transparency_data is False
            with pytest.raises(NotImplementedError):
                image.image_resources = image_resources
            with pytest.raises(NotImplementedError):
                image.global_layer_resources = global_layer_resources
            with pytest.raises(NotImplementedError):
                image.active_layer = active_layer
            with pytest.raises(NotImplementedError):
                image.has_transparency_data = True

    def test_save_official_mutation_persists(self):
        output_file = self.get_persistent_artifact_path("official_style_layer_mutation.psd")

        with PsdImage.load(self.get_test_data_path("test.psd")) as image:
            image.layers[0].name = "Official style"
            image.layers[0].left = 10
            image.layers[0].top = 20
            image.layers[0].right = 40
            image.layers[0].bottom = 60
            image.layers[0].blend_mode_key = BlendMode.Multiply
            image.save(output_file)

        with PsdImage.load(output_file) as reloaded:
            assert reloaded.layers[0].name == "Official style"
            assert reloaded.layers[0].bounds == Rectangle(0, 0, 30, 40)
            assert reloaded.layers[0].left == 10
            assert reloaded.layers[0].top == 20
            assert reloaded.layers[0].right == 40
            assert reloaded.layers[0].bottom == 60
            assert reloaded.layers[0].blend_mode_key == BlendMode.Multiply
