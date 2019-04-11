using JDFTools;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace JDFToolsTests
{
    [TestClass]
    public class SignaJDFTests
    {
        public SignaJDF TestJDF { get; set; }
        public SignaJDF VersionedJDF { get; set; }
        public void TestSetup()
        {
            TestJDF = new SignaJDF("../../../../JDFTools/TestData/data.jdf");
            VersionedJDF = new SignaJDF("../../../../JDFTools/TestData/data-Versioned.jdf");
        }
        [TestMethod]
        public void ResourcePoolTest()
        {
            //Arrange
            TestSetup();
            //Act
            var resourcePool1 = TestJDF.ResourcePool;
            var resourcePool2 = VersionedJDF.ResourcePool;
            //Assert
            Assert.IsNotNull(resourcePool1);
            Assert.IsNotNull(resourcePool2);
        }
        [TestMethod]
        public void LayoutTest()
        {
            //Arrange
            TestSetup();
            //Act
            var layout1 = TestJDF.Layout;
            var layout2 = VersionedJDF.Layout;
            //Assert
            Assert.IsNotNull(layout1);
            Assert.IsNotNull(layout2);
        }
        [TestMethod]
        public void BlobTest()
        {
            //Arrange
            TestSetup();
            //Act
            var blob1 = TestJDF.Blob;
            var blob2 = VersionedJDF.Blob;
            //Assert
            Assert.IsNotNull(blob1);
            Assert.IsNotNull(blob2);
        }
    }
}
