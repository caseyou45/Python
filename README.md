# Python

 
This Python application generates random numbers (example: .91231254) from natural sources. Users can select from two variations already prepared. 
The application will create image frames from livestreams found on YouTube. It will then use those frames to perform the analysis.  

One generates random numbers based on the presence and movement of jellyfish in a tank at the Monterey Bay Aquarium. 
The photo is sectioned off into nine sections. The program then simply looks for the redness of jellyfish. If found, then this process is followed: 

  1) Create a decimal equivalent of the section of the photo we are in (example: 8 = .8) 
  2) Then add that value to how much red is in the pixel (32 / 255 == .125 / 10 = .0125) 
  3) So the resulting number is based on where the jelly is and how red it appears (.8125) 

The second method simply looks for the difference between the frames. In this case, it’s a street in Japan. 
A similar logic like described above is then applied if enough difference is detected.  

A third option exists for users to input their own URL while using the second method explained above.  

The application’s output is a folder containing the random numbers, a comparison of how those numbers compare to what Python’s 
output is with the same amount of numbers, and a sample of the frames used to create the analysis.  
