(* ::Package:: *)

(* ::Text:: *)
(*\:70b9\:4f4d\:4fe1\:606f\:539f\:59cb\:6570\:636e\:6765\:81ea\:9999\:6e2f\:7279\:533a\:73af\:5883\:90e8\:95e8\:5730\:8868\:6c34\:8d28\:91cf\:5e74\:62a5, \:4e3aPDF\:6587\:4ef6\:4e2d\:7684\:8868\:683c. *)
(*\:7531\:4e8e\:8868\:683c\:4e2d\:7684\:6587\:5b57\:5728\:76f4\:63a5\:590d\:5236\:7c98\:8d34\:81f3\:6587\:672c\:65f6\:51fa\:73b0\:6392\:7248\:9519\:4e71, \:56e0\:6b64\:9700\:8981\:624b\:52a8\:8c03\:6574\:6392\:7248: *)


(* ::Program:: *)
(*Shing Mun River*)
(*KY1 22\[Degree] 21' 39.8" N 114\[Degree] 12' 32.0" E*)
(*TR17 22\[Degree] 23' 47.5" N 114\[Degree] 11' 41.4" E*)
(*...*)
(*Lam Tsuen River*)
(*TR12 22\[Degree] 27' 01.9" N 114\[Degree] 09' 27.9" E*)
(*TR12B 22\[Degree] 27' 41.0" N 114\[Degree] 08' 49.6" E*)
(*...*)


	Begin["AquaticEnvironMonitoring`"]; 


		WaterPollutionSpotExtract[filename_String] := 
		Block[{strm, siteRecFilter, siteNameFilter, stringLine, 
				aquaName, siteName, siteNameIndex, siteCoordDescr, siteCoord, siteInfo}, 
			(*Read file serially. *)
			strm = Import[filename, "Text", CharacterEncoding->"UTF-8"]//StringToStream; 
			(*Site name is at the beginning of a row, followed by coordinates of sites seperated by whitespace. *)
			siteRecFilter = RegularExpression["^([0-9A-Z]+) .*\[Degree] .*' .*\" N .*\[Degree] .*' .*\" E$"]; 
			siteNameFilter = RegularExpression["[A-Z]+[0-9]*[A-Z]*\\w"]; 
			stringLine = ""; strm//SetStreamPosition[#, 0]&; aquaName = ""; siteCoordDescr = ""; 
			siteInfo = Reap[
				While[stringLine =!= EndOfFile,
					(*Sequantially read filestream by line. *)
					stringLine = strm//Read[#, String]&; 
					If[stringLine == EndOfFile, 
						Break[]; 
					]; 
					stringLine = stringLine//StringTrim; 
					Which[
					(*Name of rivers. *)
					Not@StringMatchQ[stringLine, siteRecFilter], 
						aquaName = stringLine//List; 
					, True, 
						(*Extract the ID of sites. *)
						siteNameIndex = StringPosition[stringLine, siteNameFilter, 1]//First; 
						siteName = StringTake[stringLine, siteNameIndex]//StringTrim//List; 
						(*Extract and parse lat. and lon. of sites. *)
						siteCoordDescr = StringTake[stringLine, {Last@siteNameIndex + 1, -1}]//StringReplace[#,"\[CapitalAHat]"->""]&;
						siteCoord=FromDMS[siteCoordDescr]; 
						Sow[Join[aquaName, siteName, siteCoord]]; 
					];
				];
			][[2, 1]];
			strm//Close; 
			Return[siteInfo]; 
		];


	End[]; 
