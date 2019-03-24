using System;
using System.Collections.Generic;
using System.Xml;
using System.Xml.XPath;

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

    class Program
    {

        static void Main(string[] args)
        {
            XmlDocument xml = new XmlDocument();
            xml.Load("data.jdf");

            var jDF = new SignaJDF(xml);
            List<string> jobParts = jDF.GetJobParts();
            foreach (string part in jobParts)
            {
                Console.WriteLine(part);
            }
            
            Console.ReadKey();
        }
    }
}
