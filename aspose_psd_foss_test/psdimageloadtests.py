using Aspose.PSD;
using Aspose.PSD.FileFormats.Core.Blending;
using Aspose.PSD.FileFormats.Psd;
using System.IO;
using NUnit.Framework;

namespace Aspose.PSD.FOSS.Tests;

/// <summary>
/// Contains PSD ImageLoad tests.
/// </summary>
public sealed class PsdImageLoadTests : PsdTestFixtureBase
{

    /// <summary>
    /// Tests that loading a PSD file returns correct document properties.
    /// Verifies image dimensions, channels, bits per channel, color mode, version, and layer count.
    /// </summary>
    [Test]
    public void Load_Document_ReadsProperties()
    {
        string testFile = Path.Combine(TestContext.CurrentContext.TestDirectory, "testdata", "test.psd");

        Assert.That(File.Exists(testFile), Is.True, "Test file not found");

        using var image = PsdImage.Load(testFile);

        Assert.That(image.Width, Is.GreaterThan(0));
        Assert.That(image.Height, Is.GreaterThan(0));
        Assert.That(image.Channels, Is.GreaterThan(0));
        Assert.That(image.BitsPerChannel, Is.EqualTo(8));
        Assert.That(image.ColorMode, Is.EqualTo(ColorModes.Rgb));
        Assert.That(image.Version, Is.GreaterThan(0).And.LessThanOrEqualTo(6));
        Assert.That(image.Layers.Length, Is.GreaterThan(0));
    }


    /// <summary>
    /// Tests that loading a PSD file returns correct layer properties.
    /// Verifies layer count, bounds, visibility, opacity, and blend mode.
    /// </summary>
    [Test]
    public void Load_Layer_ReadsProperties()
    {
        string testFile = Path.Combine(TestContext.CurrentContext.TestDirectory, "testdata", "test.psd");

        using var image = PsdImage.Load(testFile);

        Assert.That(image.Layers.Length, Is.GreaterThan(0));

        var firstLayer = image.Layers[0];

        Assert.That(firstLayer.Name, Is.EqualTo("Background copy"));
        Assert.That(firstLayer.Bounds, Is.Not.EqualTo(default(Rectangle)));
        Assert.That(firstLayer.IsVisible, Is.True);
        Assert.That(firstLayer.Opacity, Is.GreaterThanOrEqualTo(0).And.LessThanOrEqualTo(255));
        Assert.That(firstLayer.BlendModeKey, Is.EqualTo(BlendMode.Normal));

        Assert.That(image.Layers[1].Name, Is.EqualTo("Pattern Fill 1"));
    }


    /// <summary>
    /// Tests that layers can be accessed by index.
    /// </summary>
    [Test]
    public void Load_Layers_Indexable()
    {
        string testFile = Path.Combine(TestContext.CurrentContext.TestDirectory, "testdata", "test.psd");

        using var image = PsdImage.Load(testFile);

        Assert.That(image.Layers[0], Is.Not.Null);
        Assert.That(image.Layers[1], Is.Not.Null);
    }


    /// <summary>
    /// Tests that loading from a seekable stream preserves the original stream position.
    /// </summary>
    [Test]
    public void Load_Seekable_PreservesPosition()
    {
        byte[] bytes = File.ReadAllBytes(Path.Combine(TestContext.CurrentContext.TestDirectory, "testdata", "test.psd"));
        byte[] prefix = [1, 2, 3, 4, 5];
        using var stream = new MemoryStream();
        stream.Write(prefix);
        stream.Write(bytes);
        stream.Position = prefix.Length;

        using var image = PsdImage.Load(stream);

        Assert.That(stream.Position, Is.EqualTo(prefix.Length));
        Assert.That(image.Width, Is.GreaterThan(0));
    }


    /// <summary>
    /// Tests that loading from a non-seekable stream still succeeds.
    /// </summary>
    [Test]
    public void Load_NonSeekableStream_Succeeds()
    {
        byte[] bytes = File.ReadAllBytes(Path.Combine(TestContext.CurrentContext.TestDirectory, "testdata", "test.psd"));
        using var stream = new NonSeekableReadStream(bytes);
        using var image = PsdImage.Load(stream);

        Assert.That(image.Width, Is.GreaterThan(0));
        Assert.That(image.Layers.Length, Is.GreaterThan(0));
    }


    /// <summary>
    /// Tests that loading from a null stream throws <see cref="ArgumentNullException"/>.
    /// </summary>
    [Test]
    public void Load_NullStream_Throws()
    {
        Assert.That(() => PsdImage.Load((Stream)null!), Throws.InstanceOf<ArgumentNullException>());
    }


    /// <summary>
    /// Tests that loading a missing file path throws <see cref="FileNotFoundException"/>.
    /// </summary>
    [Test]
    public void Load_MissingFile_Throws()
    {
        string missingFile = Path.Combine(_testDir, "missing.psd");
        Assert.That(() => PsdImage.Load(missingFile), Throws.InstanceOf<FileNotFoundException>());
    }


    /// <summary>
    /// Tests that loading a file with an invalid signature throws <see cref="PsdLoadException"/>.
    /// </summary>
    [Test]
    public void Load_InvalidSignature_Throws()
    {
        using var stream = new MemoryStream(BuildHeaderBytes(PsdHeader.PsdVersion));
        using var reader = new BigEndianReader(stream, leaveOpen: true);
        stream.Position = 0;
        stream.WriteByte((byte)'B');
        stream.Position = 0;

        Assert.That(() => PsdHeader.Load(reader), Throws.InstanceOf<PsdLoadException>());
    }


    /// <summary>
    /// Tests that simple document-level inspection properties expose the parsed structural state.
    /// </summary>
    [Test]
    public void Load_DocInspection_Reads()
    {
        using var image = PsdImage.Load(Path.Combine(TestContext.CurrentContext.TestDirectory, "testdata", "test.psd"));

        Assert.That(image.Header, Is.Not.Null);
        Assert.That(image.IsLargeDocument, Is.False);
        Assert.That(image.IsPsb, Is.False);
        Assert.That(image.LayerCount, Is.EqualTo(2));
        Assert.That(image.HasImageResources, Is.True);
        Assert.That(image.ResourceCount, Is.EqualTo(26));
        Assert.That(image.HasColorModeData, Is.False);
        Assert.That(image.HasMergedImageData, Is.True);
        Assert.That(image.Compression, Is.EqualTo(CompressionMethod.RLE));
        Assert.That(image.ImageDataKind, Is.EqualTo(ImageDataKind.Rle));
        Assert.That(image.UsesPrediction, Is.False);
        Assert.That(image.Version, Is.EqualTo(6));
        Assert.That(image.Header.Version, Is.EqualTo(PsdHeader.PsdVersion));
        Assert.That(image.Header.ColorMode, Is.EqualTo(image.ColorMode));
    }
}
