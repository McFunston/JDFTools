using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace JDFTools.Models
{
    class Equipment
    {
        public string Name { get; set; }
        public bool Perfecting { get; set; }
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
                PrintingPresses = JsonConvert.DeserializeObject<List<Equipment>>(json);
            }
        }

        public List<Equipment> PrintingPresses { get; set; }
    }

}
