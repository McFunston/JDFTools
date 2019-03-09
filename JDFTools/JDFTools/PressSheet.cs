using System.Collections.Generic;

namespace JDFTools
{
    public class PressSheet : Box
    {
        public PressSheet(float[] borders) : base(borders)
        {

        }
        public List<Page> Pages{ get; set; }

        public string WorkStyle { get; set; }

    }
}
