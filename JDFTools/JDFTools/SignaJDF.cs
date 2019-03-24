using System;
using System.Collections.Generic;
using System.Xml;
using System.Xml.Linq;

namespace JDFTools
{
    public class SignaPage
    {
        public string DescriptiveName { get; set; }
        public float[] FinalPageBox { get; set; }
        public string JobPart { get; set; }
        public string Signature { get; set; }
        public string Side { get; set; }
        public int Orientation { get; set; }
        public int Order { get; set; }

    }
    public class SignaSignature
    {
        public string Name { get; set; }
    }
    public class SignaSheet
    {
        public string Name { get; set; }

    }

    public class SignaJDF 
    {
        public SignaJDF(XmlDocument xmlDocument)
        {
            sourceXML = xmlDocument;
            NameSpaceManager = new XmlNamespaceManager(sourceXML.NameTable);
            NameSpaceManager.AddNamespace("default", "http://www.CIP4.org/JDFSchema_1_1");
        }

        public XmlNamespaceManager NameSpaceManager { get; set; }

        private void GetPages()
        {

        }

        XmlDocument sourceXML;

        public string JobID => sourceXML.DocumentElement.Attributes["JobID"].Value;

        public XmlElement ResourcePool => (XmlElement)sourceXML.
            SelectSingleNode("//default:ResourcePool", NameSpaceManager);

        public XmlElement Layout => (XmlElement)ResourcePool.
            SelectSingleNode("default:Layout", NameSpaceManager);

        public XmlNodeList Layouts => sourceXML.GetElementsByTagName("Layout");

        public XmlNodeList Signatures => Layout.
            SelectNodes("//default:Layout[@SignatureName]", NameSpaceManager);

        public XmlNodeList PressSheets => Layout.
            SelectNodes("//default:Layout[@SheetName]", NameSpaceManager);

        public XmlNodeList Pages => Layout.
            SelectNodes("//default:ContentObject", NameSpaceManager);


        public List<String> GetJobParts()
        {
            var sigs = Signatures;
            List<String> jobPartList = new List<string>();
            XmlNode jobParts = ResourcePool.SelectSingleNode("//default:SignaJob", NameSpaceManager);
            foreach (XmlNode jobPart in jobParts)
            {
                jobPartList.Add(jobPart.Attributes.GetNamedItem("Name").Value);
            }
            return jobPartList;
        }

        public List<string> GetLayoutNames()
        {
            List<string> layoutNames = new List<string>();
            
            foreach (XmlElement layout in Layouts)
            {
                
                if (layout.HasAttribute("SheetName"))
                {
                    layoutNames.Add(layout.GetAttribute("SheetName"));
                }
                
            }
            return layoutNames;
        }

    }
}
