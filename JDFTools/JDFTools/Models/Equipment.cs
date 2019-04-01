using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace JDFTools.Models
{

    public class Equipment
    {
        public Press[] Presses { get; set; }
    }

    public class Press
    {
        public string Name { get; set; }
        public string Perfecting { get; set; }
        public string Type { get; set; }
        public float PlateWidth { get; set; }
        public float PlateHeight { get; set; }
    }

    class EquipmentList
    {
        public EquipmentList()
        {
            using (StreamReader r = new StreamReader("Equipment.json"))
            {
                var json = r.ReadToEnd();
                PrintingPresses = JsonConvert.DeserializeObject<List<Press>>(json);
            }
        }

        public List<Press> PrintingPresses { get; set; }

        public string PressDetector(float PlateWidth, float PlateHeight)
        {
            string pressName = "Unknown";
            foreach (Press press in PrintingPresses)
            {
                if (press.PlateHeight == PlateHeight && press.PlateWidth == PlateWidth)
                {
                    pressName = press.Name;
                }
            }

            return pressName;
        }
    }

}
