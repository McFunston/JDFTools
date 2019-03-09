﻿using System;
using System.Collections.Generic;
using System.Text;

namespace JDFTools
{
    enum BindingStyleType { PerfectBound, SaddleStitch, Loose}
    class ProductPart
    {
        public string Name { get; set; }
        public BindingStyleType BindingStyle { get; set; }
        public List<PressSheet> PressSheets { get; set; }
    }
}
