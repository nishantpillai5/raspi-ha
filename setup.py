from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='raspi_ha',
      version='0.1',
      description='Raspberry Pi Home automation with Oled display, PIR sensor, IR Reciever, Temp sensor and Relays',
      long_description=readme(),
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2.7'],
      keywords='raspberry pi home automation oled relays',
      url='http://github.com/nishantpillai5/raspi-ha',
      author='Nishant Pillai',
      author_email='something@example.com',
      license='GNU GPL v3',
      packages=['raspi_ha'],
      dependency_links=['http://github.com/rm-hull/luma.oled',
                        'http://github.com/adafruit/Adafruit_Python_DHT'],
      scripts=['bin/raspi_ha'],
      zip_safe=False)
