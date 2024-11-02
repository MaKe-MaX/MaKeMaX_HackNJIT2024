using UnityEngine
using System.Collections
using System.IO.Ports;

public class Joystick : MonoBehavior
{
    SerialPort data_stream - new SerialPort("COM5", 19200);
    public string recievedstring;
    public string[] data;

    void Start()
    {
        data_stream.Open();
    }

    void Update()
    {
        recievedstring = data_stream.ReadLine();
        string[] data = recievedstring.Split(',');

    }

}