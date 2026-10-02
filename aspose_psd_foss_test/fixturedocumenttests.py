import os
import struct

from aspose_psd_foss_test.psdtestfixturebase import PsdTestFixtureBase
from aspose_psd_foss.psdimage import PsdImage
from aspose_psd_foss.colormodes import ColorModes
from aspose_psd_foss.psdheader import PsdHeader
from aspose_psd_foss.compressionmethod import CompressionMethod
from aspose_psd_foss.layers.blendmode import BlendMode


class TestFixtureDocument(PsdTestFixtureBase):
    def test_load_basic_rgb_reads_metadata(self):
        image = PsdImage.load(self.getTestDataPath("basic-rgb.psd"))
        assert image.width == 200
        assert image.height == 200
        assert image.channels == 3
        assert image.bitsPerChannel == 8
        assert image.colorMode == ColorModes.Rgb
        assert image.version == 6
        assert image.header.version == PsdHeader.PsdVersion
        assert image.layerCount == 3
        assert image.resourceCount == 26
        assert image.compression == CompressionMethod.RLE

    def test_save_basic_rgb_is_byte_exact(self):
        self.assertByteExactRoundTrip("basic-rgb.psd")

    def test_save_basic_rgb_renames_layer(self):
        self.assertRenameSave("basic-rgb.psd", layerIndex=1, newName="Renamed Rectangle")

    def test_load_basic_cmyk_reads_metadata(self):
        image = PsdImage.load(self.getTestDataPath("basic-cmyk.psd"))
        assert image.width == 200
        assert image.height == 200
        assert image.channels == 4
        assert image.colorMode == ColorModes.Cmyk
        assert image.layerCount == 3
        assert image.resourceCount == 28
        assert image.compression == CompressionMethod.RLE
        assert len(image.imageDataInfo.rowByteCounts) == 800

    def test_save_basic_cmyk_is_byte_exact(self):
        self.assertByteExactRoundTrip("basic-cmyk.psd")

    def test_load_basic_psb_reads_metadata(self):
        image = PsdImage.load(self.getTestDataPath("basic.psb"))
        assert image.version == 6
        assert image.header.version == PsdHeader.PsbVersion
        assert image.isLargeDocument is True
        assert image.isPsb is True
        assert image.width == 200
        assert image.height == 200
        assert image.layerCount == 0
        assert image.resourceCount == 24
        assert image.compression == CompressionMethod.RLE
        assert image.imageDataInfo.rowLengthFieldSize == struct.calcsize("I")

    def test_save_basic_psb_is_byte_exact(self):
        self.assertByteExactRoundTrip("basic.psb")

    def test_load_layered_psb_reads_layers(self):
        image = PsdImage.load(self.getTestDataPath("layered.psb"))
        assert image.version == 6
        assert image.header.version == PsdHeader.PsbVersion
        assert image.layerCount == 3
        assert image.layers[0].name == "Background"
        assert image.layers[1].name == "Rectangle 1"
        assert image.layers[2].name == "Ellipse 1"
        assert image.layers[2].opacity == 191

    def test_save_layered_psb_renames_layer(self):
        self.assertRenameSave("layered.psb", layerIndex=1, newName="Renamed Rectangle")

    def test_save_layered_psb_changes_blend_mode(self):
        test_file = self.getTestDataPath("layered.psb")
        output_file = self.getPersistentArtifactPath("layered_psb_blend_mode_test.psb")
        image = PsdImage.load(test_file)
        image.layers[1].blendModeKey = BlendMode.Multiply
        image.save(output_file)
        self.logArtifactDirectory(output_file)
        reloaded = PsdImage.load(output_file)
        assert reloaded.layers[1].blendModeKey == BlendMode.Multiply

    def test_load_layer_variants_reads_flags(self):
        image = PsdImage.load(self.getTestDataPath("layer-variants.psd"))
        assert image.layerCount == 4
        assert image.layers[1].isVisible is False
        assert image.layers[2].blendModeKey == BlendMode.LinearBurn
        assert image.layers[2].rawBlendModeKey == "lbrn"
        assert image.layers[3].clipping == 1
        assert len(image.layers[3].additionalLayerData) > 0

    def test_save_layer_variants_clipping(self):
        test_file = self.getTestDataPath("layer-variants.psd")
        output_file = self.getPersistentArtifactPath("layer_variants_clipping_test.psd")
        image = PsdImage.load(test_file)
        image.layers[3].clipping = 0
        image.save(output_file)
        self.logArtifactDirectory(output_file)
        reloaded = PsdImage.load(output_file)
        assert reloaded.layers[3].clipping == 0

    def test_save_layer_variants_preserves_tail(self):
        test_file = self.getTestDataPath("layer-variants.psd")
        with open(test_file, "rb") as f:
            original_bytes = f.read()
        output_file = self.getPersistentArtifactPath("layer_variants_tail_test.psd")
        image = PsdImage.load(test_file)
        image.layers[2].name = "Ellipse 1 Updated"
        image.save(output_file)
        self.logArtifactDirectory(output_file)
        with open(output_file, "rb") as f:
            saved_bytes = f.read()
        assert self.readLayerAndMaskTail(saved_bytes) == self.readLayerAndMaskTail(original_bytes)
