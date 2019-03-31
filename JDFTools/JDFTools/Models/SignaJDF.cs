using System;
using System.Collections.Generic;
using System.Xml;
using System.Xml.Linq;

namespace JDFTools
{
    public class SignaPage
    {
        public SignaPage(XmlNode contentObject)
        {
            DescriptiveName = contentObject.Attributes["DescriptiveName"].Value;
            string[] fpb = contentObject.Attributes["HDM:FinalPageBox"].Value.Split(" ");
            float[] FinalPageBox = new float[4];
            FinalPageBox[0] = float.Parse(fpb[0]);
            FinalPageBox[1] = float.Parse(fpb[1]);
            FinalPageBox[2] = float.Parse(fpb[2]);
            FinalPageBox[3] = float.Parse(fpb[3]);
            Signature = contentObject.ParentNode.ParentNode.Attributes["Name"].Value;
            JobPart = contentObject.Attributes["HDM:JobPart"].Value;
            Side = contentObject.Attributes["HDM:AssemblyFB"].Value;
            Orientation = int.Parse(contentObject.Attributes["HDM:PageOrientation"].Value);
            Order = int.Parse(contentObject.Attributes["Ord"].Value);
        }

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
            NameSpaceManager.AddNamespace("HDM", "www.heidelberg.com/schema/HDM");
        }

        public XmlNamespaceManager NameSpaceManager { get; set; }

        public void GetPages()
        {
            SignaPages = new List<SignaPage>();
            foreach (XmlNode contentObject in ContentObjects)
            {
                SignaPage signaPage = new SignaPage(contentObject);
                SignaPages.Add(signaPage);
            }


        }

        XmlDocument sourceXML;
        public List<SignaPage> SignaPages { get; set; }
        public string JobID => sourceXML.DocumentElement.Attributes["JobID"].Value;
        public string DescriptiveName => sourceXML.DocumentElement.Attributes["DescriptiveName"].Value;
        public string Creator => GenContext.Attributes["OS_User"].Value;
        public string Client => ClientInfo.Attributes["CustomerID"].Value;
        public string Version => GenContext.Attributes["ProductMajorVersion"].Value;
        public string CreationTime => Blob.Attributes["TimeStamp"].Value;

        public XmlElement ResourcePool => (XmlElement)sourceXML.
            SelectSingleNode("//default:ResourcePool", NameSpaceManager);

        public XmlElement Layout => (XmlElement)ResourcePool.
            SelectSingleNode("default:Layout", NameSpaceManager);

        public XmlNodeList Signatures => Layout.
            SelectNodes("//default:Layout[@SignatureName]", NameSpaceManager);

        public XmlNodeList LayerList => Layout.
            SelectNodes("//default:LayerList", NameSpaceManager);

        public XmlNodeList PressSheets => Layout.
            SelectNodes("//default:Layout[@SheetName]", NameSpaceManager);

        public XmlNodeList Pages => Layout.
            SelectNodes("//default:ContentObject", NameSpaceManager);

        public XmlNodeList JobParts => Layout.
            SelectNodes("//default:SignaJobPart", NameSpaceManager);

        public XmlNode Created => Layout.
            SelectSingleNode("//default:AuditPool/default:Created", NameSpaceManager);

        public XmlNode GenContext => Layout.
            SelectSingleNode("//default:SignaGenContext",NameSpaceManager);

        public XmlNode ClientInfo => ResourcePool.
            SelectSingleNode("//default:CustomerInfo", NameSpaceManager);

        public XmlNode Blob => Layout.
            SelectSingleNode("default:SignaBLOB", NameSpaceManager);

        public XmlNodeList ContentObjects => Layout.
            SelectNodes("//default:ContentObject", NameSpaceManager);

        public List<String> GetJobParts()
        {
            var sb = Blob;            
            List<String> jobPartList = new List<string>();
            //XmlNode jobParts = ResourcePool.SelectSingleNode("//default:SignaJob", NameSpaceManager);
            //foreach (XmlNode jobPart in jobParts)
            //{
            //    jobPartList.Add(jobPart.Attributes.GetNamedItem("Name").Value);
            //}
            return jobPartList;
        }

        //public List<string> GetLayoutNames()
        //{
        //    List<string> layoutNames = new List<string>();
            
        //    foreach (XmlElement layout in Layouts)
        //    {
                
        //        if (layout.HasAttribute("SheetName"))
        //        {
        //            layoutNames.Add(layout.GetAttribute("SheetName"));
        //        }
                
        //    }
        //    return layoutNames;
        //}

    }
}
