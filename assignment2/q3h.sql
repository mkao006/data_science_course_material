SELECT sum(t1.count * t2.count)
       FROM Frequency t1
       JOIN Frequency t2
       WHERE t1.docid == "10080_txt_crude"
       AND t2.docid == "17035_txt_earn"
       AND t1.term == t2.term;
