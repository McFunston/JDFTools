using System;
using System.Collections.Generic;
using System.Xml;
using System.Xml.Linq;

namespace JDFTools
{
    public static class AttributeTools
    {
        public static float[] SplitBox(string box)
        {
            float[] splitBox = new float[4];
            string[] boxArray = box.Split(" ");

            splitBox[0] = float.Parse(boxArray[0]);
            splitBox[1] = float.Parse(boxArray[1]);
            splitBox[2] = float.Parse(boxArray[2]);
            splitBox[3] = float.Parse(boxArray[3]);
            return splitBox;
        }
    }
    public class SignaPage
    {

        public SignaPage(XmlNode contentObject)
        {
            DescriptiveName = contentObject.Attributes["DescriptiveName"].Value;
            string fpb = contentObject.Attributes["HDM:FinalPageBox"].Value;
            FinalPageBox = AttributeTools.SplitBox(fpb);
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
        public string DescriptiveName { get; set; }
        public string WorkStyle { get; set; }

        public List<SignaSide> SignaSides { get; set; }
        public List<SignaPage> SignaPages { get; set; }

        public float[] PlateBox => SignaSides[0].PlateBox;
        public float[] SheetBox => SignaSides[0].SheetBox;

        public SignaSignature(XmlNode signature, List<SignaSide> signaSides, List<SignaPage> signaPages)
        {
            Name = signature.Attributes["Name"].Value;
            DescriptiveName = signature.Attributes["DescriptiveName"].Value;
            WorkStyle = signature.Attributes["SourceWorkStyle"].Value;
            SignaSides = new List<SignaSide>();
            SignaPages = new List<SignaPage>();
            foreach (SignaSide signaSide in signaSides)
            {
                if (signaSide.Signature == Name)
                {
                    SignaSides.Add(signaSide);
                    SignaPages.AddRange(signaSide.Pages);
                }
            }

        }
    }
    public class SignaSide
    {
        public SignaSide(XmlNode xmlNode, List<SignaPage> signaPages)
        {
            Name = xmlNode.Attributes["Side"].Value;
            Signature = xmlNode.ParentNode.Attributes["Name"].Value;
            SheetBox = AttributeTools.SplitBox(xmlNode.Attributes["HDM:PaperRect"].Value);
            PlateBox = AttributeTools.SplitBox(xmlNode.
                ParentNode.Attributes["SurfaceContentsBox"].Value);
            Pages = new List<SignaPage>();
            foreach (var page in signaPages)
            {
                if (page.Signature == Signature && page.Side == Name)
                {
                    Pages.Add(page);
                }
            }
        }

        public string Name { get; set; }
        public string Signature { get; set; }
        public float[] PlateBox { get; set; }
        public float[] SheetBox { get; set; }
        public List<SignaPage> Pages { get; set; }
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

        public void GetSides()
        {
            if (SignaPages == null) { this.GetPages(); };
            SignaSides = new List<SignaSide>();
            foreach (XmlNode side in Sides)
            {
                SignaSide signaSide = new SignaSide(side, SignaPages);
                SignaSides.Add(signaSide);
            }
        }

        public void GetSignatures()
        {
            if (SignaSides == null) { this.GetSides(); }
            SignaSignatures = new List<SignaSignature>();
            foreach (XmlNode signature in PressSheets)
            {
                SignaSignature signaSignature = new SignaSignature(signature, SignaSides, SignaPages);
                SignaSignatures.Add(signaSignature);
            }

        }

        XmlDocument sourceXML;
        public List<SignaPage> SignaPages { get; set; }
        public List<SignaSide> SignaSides { get; set; }
        public List<SignaSignature> SignaSignatures { get; set; }
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

        public XmlNodeList Sides => Layout.
            SelectNodes("//default:Layout[@Side]", NameSpaceManager);

        public XmlNodeList Pages => Layout.
            SelectNodes("//default:ContentObject", NameSpaceManager);

        public XmlNodeList JobParts => Layout.
            SelectNodes("//default:SignaJobPart", NameSpaceManager);

        public XmlNode Created => Layout.
            SelectSingleNode("//default:AuditPool/default:Created", NameSpaceManager);

        public XmlNode GenContext => Layout.
            SelectSingleNode("//default:SignaGenContext", NameSpaceManager);

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
