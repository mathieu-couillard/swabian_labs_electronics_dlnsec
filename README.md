# swabian_labs_electronics_dlnsec
Python driver for for Swabian Labs Electronics DLnSec laser

# Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Requirements
numpy  
pyvisa  
pyvisa-py

# Usage
This drivers contains simple functions for all the quasi-SCPI commands that control the Swabian/Labs Electronics dlnsec laser. Some commands are redundant but are useful when trying to remember commands in an interactive Python terminal (ex. CW() and continuous_wave() do the same this). The first argument passed in the constructor is the address as used by pyvisa. Commands like power() that have a write and query function are a query when no argument is enter and write when an argument is entered (ex.: .power() with return the current power while power(50) will set the power to 50%).

The basic functionality is shown below
```
from swabian_dlnsec import DLnSec
import pyvisa as visa

rm = visa.ResourceManager('py')
print(rm.list_resources())
laser = DLnSec('DEVICE ADDRESS', verbatim=True) # replace 'DEVICE ADDRESS' with the one returned from rm.list_resources()
print(laser.identify()) 
print(laser.power(15)) # 15% power
print(laser.cw()) # coninuous wave
print(laser.power()) # query power
```
