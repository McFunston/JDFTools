using System;
using System.Collections.Generic;
using System.Xml;

namespace JDFTools
{
    public class SignaJDF 
    {
        public SignaJDF(XmlDocument xmlDocument)
        {
            sourceXML = xmlDocument;
        }

        XmlDocument sourceXML;

        public string JobID
        {
            get { return sourceXML.DocumentElement.Attributes["JobID"].Value; }
        }

        public XmlElement ResourcePool => (XmlElement)sourceXML.GetElementsByTagName("ResourcePool")[0];

        public XmlElement Layout => (XmlElement)ResourcePool.GetElementsByTagName("Layout")[0];

        public XmlNodeList Layouts => sourceXML.GetElementsByTagName("Layout");

        public List<String> GetJobParts()
        {
            List<String> jobPartList = new List<string>();
            XmlNode jobParts = XMLTools.FindNode(Layout.ChildNodes, "SignaJob");
            foreach (XmlNode jobPart in jobParts)
            {
                jobPartList.Add(jobPart.Attributes.GetNamedItem("Name").Value);
            }
            return jobPartList;
        }

        private XmlNode getResourcePool() //Get the JDF file's ResourcePool Node
        {
            XmlNodeList resourcePool = sourceXML.GetElementsByTagName("ResourcePool");
            return resourcePool[0];
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
