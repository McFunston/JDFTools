namespace JDFTools
{
    public abstract class Box
    {
        readonly float[] borders = new float[4];

        public Box(float[] borders)
        {
            if (borders.Length==4)
            {
                this.borders = borders;
            }
        }

        public float Height
        {
            get { return (borders[2]-borders[0])/72; }
        }
        public float Width
        {
            get { return (borders[3] - borders[1])/72; }
        }
    }
}
