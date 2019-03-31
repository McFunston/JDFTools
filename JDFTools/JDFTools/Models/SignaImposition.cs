using System;
using System.Collections.Generic;
using System.Text;

namespace JDFTools.Models
{
    class SignaImposition
    {
        public string JobId { get; set; }
        public string Name { get; set; }
        public string Creator { get; set; }
        public string Client { get; set; }
        public int Versions { get; set; }
        public string SignaVersion { get; set; }
        public DateTime CreationTime { get; set; }
        public List<ProductPart> ProductParts { get; set; }
        SignaJDF signaJDF;

        public SignaImposition(SignaJDF signaJDF)
        {
            this.signaJDF = signaJDF ?? throw new ArgumentNullException(nameof(signaJDF));
        }
        public void GetBasicData()
        {
            JobId = signaJDF.JobID;
            Name = signaJDF.DescriptiveName;
            Creator = signaJDF.Creator;
            Client = signaJDF.Client;
            SignaVersion = signaJDF.Version;
            CreationTime = DateTime.Parse(signaJDF.CreationTime);

        }
    }
}
