# musicbox
 Creates  strips for 30 note music boxes

 This unimaginatively named program converts a DXF file of a music box strip to an SVG file suitable for a Cricut Explore Air 2. It places a leader at the beginning of the strip and, if the length of a song exceeds a specified length, breaks it up into multiple strips. Interlocking tabs are added in the case of multiple strips. It was written to support DXF files created at https://musicboxmaniacs.com/ for a 30-note hand crank music box movement.
 
 The Basic Workflow:
 * Create or select a song at https://musicboxmaniacs.com/
 * Export it as a DXF file in Grand Illusions 30 format
 * Run the program
 
 python musicbox.py
 
 * Fill in the fields in the dialog box that pops up
   * Input file
   * Output file (Include the .svg extension in the file name)
   * Length of Leader (defaults to one inch and applies only to the first strip generated)
   * Maximum Length of First Strip (Takes into account the length of the leader. Defaults to 11.5 inches, but the actual size depends on how you lay it out in Cricut's Design Space)
   
 The output SVG file is drawn at 72 dpi and contains one group per strip. Each group has a combined path of the circles (notes) and a polyline representing the outline of the strip. Each strip is 2.75 inches wide and variable in length.