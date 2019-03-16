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

        public List<String> GetJobParts()
        {
            List<String> jobPartList = new List<string>();
            XmlNode layout = getLayoutNode();
            XmlNode jobParts = XMLTools.FindNode(layout.ChildNodes, "SignaJob");
            foreach (XmlNode jobPart in jobParts)
            {
                jobPartList.Add(jobPart.Attributes.GetNamedItem("Name").Value);
            }
            return jobPartList;
        }

        private XmlNode getResourcePool() //Get the JDF file's ResourcePool Node
        {
            XmlNode resourcePool = XMLTools.FindNode(sourceXML.ChildNodes, "ResourcePool");
            return resourcePool;
        }

        private XmlNode getLayoutNode()
        {
            XmlNode resourcePool = getResourcePool();
            XmlNode layout = XMLTools.FindNode(resourcePool.ChildNodes, "Layout");
            return layout;
        }

        public List<string> GetLayoutNames()
        {
            List<string> layoutNames = new List<string>();
            XmlNodeList layouts;
            XmlElement layoutNode = (XmlElement)getLayoutNode();
            layouts = layoutNode.GetElementsByTagName("Layout");
            foreach (XmlElement layout in layouts)
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
