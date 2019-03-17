using System;
using System.Collections.Generic;
using System.Text;

namespace JDFTools.Models
{
    class Impo
    {
        public string Name { get; set; }
        public string Creator { get; set; }
        public bool Versioned { get; set; }
        public string SignaVersion { get; set; }
        public List<ProductPart> ProductParts { get; set; }
    }
}
