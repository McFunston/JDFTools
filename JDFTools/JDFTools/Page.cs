namespace JDFTools
{
    public class Page : Box
    {
        public Page(float[] borders) : base(borders)
        {

        }

        public string Name { get; set; }
        public int Order { get; set; }
        public int Orientation { get; set; }

    }
}
