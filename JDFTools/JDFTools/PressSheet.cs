using System.Collections.Generic;

namespace JDFTools
{
    public class PressSheet : Box
    {
        public PressSheet(float[] borders) : base(borders)
        {

        }
        public List<Page> Pages{ get; set; }
        private Plate[] plates;

        public Plate[] Plates
        {
            get { return plates; }
            set
            {
                if (plates == null)
                {
                    plates = new Plate[2];
                }
                plates = value;
            }
        }


        public string WorkStyle { get; set; }

    }
}
