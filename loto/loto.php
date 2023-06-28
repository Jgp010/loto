<?php
   
    $year=$_POST["year"];
    $year+=1911;
    $monuth=$_POST["monuth"];
   
    $conn=new mysqli("localhost","yy010","dkgbfdoyyy010","cloud");
    $cmd_add=
    $cmd="select * from 大樂透649彙整  where 開獎日期 like '{$year}-{$monuth}-%'";
    $re=$conn->query($cmd);
    if(!$re){
        die("查詢錯誤");
    }
    if (mysqli_num_rows($re)>0) {
        // 取得大於0代表有資料
        // while迴圈會根據資料數量，決定跑的次數
        // mysqli_fetch_assoc方法可取得一筆值
        while ($row = mysqli_fetch_assoc($re)) {
            echo"期數:".$row["期數"].",開獎日期:".$row["開獎日期"].",截止日期:".$row["截止日期"]."。<br>
            中獎號碼:".$row["n1"].",".$row["n2"].",".$row["n3"].",".$row["n4"].",".$row["n5"].",".$row["n6"]."。<br>
            特別號:".$row["spn"]."。<br>
            本期銷售金額:".$row["銷售金額"].",本期獎金總額:".$row["獎金總額"].",本期累計至下次金額:".$row["累計至下次"]."。<br>
            <hr>
            ";
        }
    }else {
        echo "查無資料";
    }
    
    mysqli_close($conn);
?>