using JDFTools.Models;
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
            //xml.Load("TestData/data.jdf");

            var jDF = new SignaJDF("TestData/data.jdf");
            var test = jDF.Sides;
            
            jDF.GetSignatures();
            var imposition = new SignaImposition(jDF);
            imposition.GetBasicData();
            var PressList = new EquipmentList();
            Console.ReadKey();
        }
    }
}
