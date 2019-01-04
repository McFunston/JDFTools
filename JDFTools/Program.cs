using System;
using System.Collections.Generic;
using System.Xml;

namespace JDFTools
{
    public static class XMLTools
    {
        static public XmlNode FindNode(XmlNodeList list, string nodeName)
        {
            if (list.Count > 0)
            {
                foreach (XmlNode node in list)
                {
                    if (node.Name.Equals(nodeName)) return node;
                    if (node.HasChildNodes)
                    {
                        XmlNode nodeFound = FindNode(node.ChildNodes, nodeName);
                        if (nodeFound != null)
                            return nodeFound;
                    }
                }
            }
            return null;
        }
    }

    public abstract class Box
    {
        readonly float[] borders = new float[4];

        public Box(float[] borders)
        {
            if (borders.Length==4)
            {
                this.borders = borders;
            }
        }

        public float Height
        {
            get { return (borders[2]-borders[0])/72; }
        }
        public float Width
        {
            get { return (borders[3] - borders[1])/72; }
        }
    }

    public class Page : Box
    {
        public Page(float[] borders) : base(borders)
        {

        }

        public string Name { get; set; }

    }

    public class PressSheet : Box
    {
        public PressSheet(float[] borders) : base(borders)
        {

        }
        public List<Page> Pages{ get; set; }

        public string WorkStyle { get; set; }

    }

    public class Plate : Box
    {
        public Plate(float[] borders) : base(borders)
        {

        }
    }

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

    class Program
    {

        static void Main(string[] args)
        {
            XmlDocument xml = new XmlDocument();
            xml.Load("data.jdf");
            var jDF = new SignaJDF(xml);
            List<string> layouts = jDF.GetLayoutNames();
            Console.WriteLine(jDF.GetJobParts());
            Console.ReadKey();
        }
    }
}
