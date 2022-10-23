using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleBuffer {
    class consize {
        static void Main(string[] args) {
            if (args.Length >= 2) {
                Console.WindowWidth = int.Parse(args[0]);
                Console.WindowHeight = int.Parse(args[1]);
            }
            if (args.Length == 4) {
                Console.BufferWidth = int.Parse(args[2]);
                Console.BufferHeight = int.Parse(args[3]);
            }
        }
    }
}
