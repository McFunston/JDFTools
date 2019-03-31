using System.Collections.Generic;

namespace JDFTools
{
    public class PressSheetSurface : Box
    {
        public PressSheetSurface(float[] borders) : base(borders)
        {

        }
        public string Name { get; set; }
        public string Press { get; set; }
        public string Side { get; set; }
        public List<Page> Pages{ get; set; }
        private Plate plates;

        public Plate Plates
        {
            get { return plates; }
            set
            {
                plates = value;
            }
        }


        public string WorkStyle { get; set; }

    }
}
