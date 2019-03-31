using System;
using System.Collections.Generic;
using System.Text;

namespace JDFTools
{
    enum BindingStyleType { PerfectBound, SaddleStitch, Loose}
    class ProductPart
    {
        public string Name { get; set; }
        public BindingStyleType BindingStyle { get; set; }
        public List<PressSheetSurface> PressSheets { get; set; }
        public List<string> Versions { get; set; }
        public int VersionCount
            {
            get { return Versions.Count; }
            }

    }
}
