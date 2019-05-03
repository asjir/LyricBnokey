LyricB

To use:
recommend.py 'artist 1' 'song 1' ['artist 2' 'song 2' ...]
 where artist1 song1 is the last track listened to
And the remaining ones are recommendations to choose from.
If only first pair is given it matches against songs already in the database.

To update database:
in /back, in order, execute:
Download data.ipynb - changing artist list whose songs to download
ELMo data.ipynb
MakePCA.ipynb - possibly adjusting n components, depending on the plot
