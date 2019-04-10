using JDFTools;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace JDFToolsTests
{
    [TestClass]
    public class UnitTest1
    {
        public SignaJDF TestJDF { get; set; }
        public SignaJDF VersionedJDF { get; set; }
        public void TestSetup()
        {
            TestJDF = new SignaJDF("../../../../JDFTools/TestData/data.jdf");
            VersionedJDF = new SignaJDF("../../../../JDFTools/TestData/data-Versioned.jdf");
        }
        [TestMethod]
        public void TestMethod1()
        {
            TestSetup();
        }
    }
}
