Realtime Stream Processsing System: Case of E-commerce


## Kappa Based Architecture


_____________________________    _____________________	     _______________________
|                           |	 |	             |	     |		           |
| [Stream Generation Layer] |	 | [Ingestion Layer] |       |	[Processing Layer] |
|       		    | => | 		     |  <==> |			   |
|      [ Data Stream ]      |	 |  [ Apache Kafka ] |	     |	 [ Apache Spark ]  |
|___________________________|    |___________________|	     |_____________________|
					     
					  |
					  V
				_______________________
				| 		      |
				| [Realtime Graphing] |
				|_____________________|
					
					   





