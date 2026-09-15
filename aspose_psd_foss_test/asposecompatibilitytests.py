import unittest
from aspose_psd_foss_test.psd_test_fixture_base import PsdTestFixtureBase
from aspose_psd_foss.image import Image
from aspose_psd_foss.psd_image import PsdImage
from aspose_psd_foss.layers.layer import Layer
from aspose_psd_foss.rectangle import Rectangle
from aspose_psd_foss.layers.blend_mode import BlendMode
from aspose_psd_foss.layers.channel_information import ChannelInformation
from aspose_psd_foss.layers.layer_blending_ranges_data import LayerBlendingRangesData
from aspose_psd_foss.point import Point
from aspose_psd_foss.size import Size
from aspose_psd_foss.color_modes import ColorModes
from aspose_psd_foss.resource_block import ResourceBlock
from aspose_psd_foss.layers.layer_resource import LayerResource
from aspose_psd_foss.layers.global_layer_mask_info import GlobalLayerMaskInfo


class AsposeCompatibilityTests(PsdTestFixtureBase, unittest.TestCase):
    def test_image_load_official_returns_psd(self):
        image = Image.load(self.get_test_data_path("test.psd"))
        psd_image = image  # type: PsdImage

        self.assertEqual(psd_image.width, 100)
        self.assertEqual(psd_image.channels_count, 3)
        self.assertEqual(len(psd_image.layers), 2)

    def test_metadata_officialtypes_reads(self):
        image = Image.load(self.get_test_data_path("test.psd"))
        psd_image = image  # type: PsdImage
        layer = psd_image.layers[0]  # type: Layer

        bounds = layer.bounds  # type: Rectangle
        blend_mode_key = layer.blend_mode_key  # type: BlendMode

        self.assertEqual(bounds, Rectangle(0, 0, 100, 100))
        self.assertEqual(blend_mode_key, BlendMode.NORMAL)
        self.assertEqual(layer.opacity, 255)
        self.assertTrue(layer.is_visible)

    def test_channels_officialshape_readsonly(self):
        image = Image.load(self.get_test_data_path("test.psd"))
        psd_image = image  # type: PsdImage
        layer = psd_image.layers[0]  # type: Layer

        channel_information = layer.channel_information  # type: list[ChannelInformation]

        self.assertEqual(layer.channels_count, len(channel_information))
        self.assertTrue(len(channel_information) > 0)
        self.assertGreater(channel_information[0].length, 0)
        with self.assertRaises(Exception):
            layer.channel_information = channel_information

    def test_layer_mask_officialshape_reads(self):
        image = Image.load(self.get_test_data_path("test.psd"))
        psd_image = image  # type: PsdImage
        layer = psd_image.layers[0]  # type: Layer

        self.assertIsNone(layer.layer_mask_data)
        self.assertEqual(len(layer.layer_blending_ranges_data), 40)
        with self.assertRaises(Exception):
            layer.layer_mask_data = None
        with self.assertRaises(Exception):
            layer.layer_blending_ranges_data = LayerBlendingRangesData()

    def test_rectangle_mutableshape_updates(self):
        rectangle = Rectangle(Point(10, 20), Size(30, 40))

        rectangle.location = Point(15, 25)
        rectangle.size = Size(35, 45)
        rectangle.right = 60
        rectangle.bottom = 80

        self.assertEqual(rectangle.x, 15)
        self.assertEqual(rectangle.y, 25)
        self.assertEqual(rectangle.width, 45)
        self.assertEqual(rectangle.height, 55)
        self.assertTrue(rectangle.contains(Point(30, 40)))
        self.assertTrue(
            rectangle.intersects_with(Rectangle.from_left_top_right_bottom(50, 70, 70, 90))
        )

        rectangle.offset(Point(5, -5))
        rectangle.inflate(Size(1, 2))

        self.assertEqual(
            rectangle,
            Rectangle.from_left_top_right_bottom(19, 18, 66, 77),
        )

    def test_image_setters_updatemetadata(self):
        image = Image.load(self.get_test_data_path("test.psd"))
        psd_image = image  # type: PsdImage
        layers = psd_image.layers
        version = psd_image.version

        psd_image.color_mode = ColorModes.RGB
        psd_image.layers = layers
        psd_image.global_angle = 45
        psd_image.version = version

        self.assertEqual(psd_image.color_mode, ColorModes.RGB)
        self.assertEqual(len(psd_image.layers), len(layers))
        self.assertEqual(psd_image.global_angle, 45)
        self.assertEqual(psd_image.version, version)

    def test_resources_officialshape_reads(self):
        image = Image.load(self.get_test_data_path("test.psd"))
        psd_image = image  # type: PsdImage

        image_resources = psd_image.image_resources  # type: list[ResourceBlock]
        global_layer_resources = psd_image.global_layer_resources  # type: list[LayerResource]
        global_layer_mask_info = psd_image.global_layer_mask_info  # type: GlobalLayerMaskInfo
        active_layer = psd_image.active_layer  # type: Layer | None

        self.assertEqual(psd_image.size, Size(psd_image.width, psd_image.height))
        self.assertTrue(len(image_resources) > 0)
        self.assertNotEqual(image_resources[0].id, 0)
        self.assertGreaterEqual(image_resources[0].data_size, 0)
        self.assertEqual(len(global_layer_resources), 0)
        self.assertIsNotNone(global_layer_mask_info)
        self.assertIs(active_layer, psd_image.layers[0])
        self.assertFalse(psd_image.is_flatten)
        self.assertFalse(psd_image.has_transparency_data)
        with self.assertRaises(Exception):
            psd_image.image_resources = image_resources
        with self.assertRaises(Exception):
            psd_image.global_layer_resources = global_layer_resources
        with self.assertRaises(Exception):
            psd_image.active_layer = active_layer
        with self.assertRaises(Exception):
            psd_image.has_transparency_data = True

    def test_save_officialmutation_persists(self):
        output_file = self.get_persistent_artifact_path("official_style_layer_mutation.psd")

        image = Image.load(self.get_test_data_path("test.psd"))
        psd_image = image  # type: PsdImage
        psd_image.layers[0].name = "Official style"
        psd_image.layers[0].left = 10
        psd_image.layers[0].top = 20
        psd_image.layers[0].right = 40
        psd_image.layers[0].bottom = 60
        psd_image.layers[0].blend_mode_key = BlendMode.MULTIPLY
        psd_image.save(output_file)

        reloaded = Image.load(output_file)
        reloaded_psd = reloaded  # type: PsdImage

        self.assertEqual(reloaded_psd.layers[0].name, "Official style")
        self.assertEqual(reloaded_psd.layers[0].bounds, Rectangle(0, 0, 30, 40))
        self.assertEqual(reloaded_psd.layers[0].left, 10)
        self.assertEqual(reloaded_psd.layers[0].top, 20)
        self.assertEqual(reloaded_psd.layers[0].right, 40)
        self.assertEqual(reloaded_psd.layers[0].bottom, 60)
        self.assertEqual(reloaded_psd.layers[0].blend_mode_key, BlendMode.MULTIPLY)
