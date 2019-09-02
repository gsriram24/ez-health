
    function myFunction(){  
        var complex = $(form).serialize(); // name1=value1&name2=value2
        var json = toSimpleJson(complex); // {"name1":"value1", "name2":"value2"}
    
        function toSimpleJson(serializedData) {
            var ar1 = serializedData.split("&");
            var json = "{";
            for (var i = 0; i<ar1.length; i++) {
                var ar2 = ar1[i].split("=");
                json += i > 0 ? ", " : "";
                json += "\"" + ar2[0] + "\" : ";
                json += "\"" + (ar2.length < 2 ? "" : ar2[1]) + "\"";
            }
            json += "}";
            return json;
            alert("Input saved");
          }   
        }
            var settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://www.google.com",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
            "processData": false,
            "data": "{\n    \"s.no\": 1,\n    \"Timestamp\": \"2014-08-27 11:29:31\",\n    \"Age\": 37,\n    \"Gender\": \"Female\",\n    \"Country\": \"United States\",\n    \"state\": \"IL\",\n    \"self_employed\": null,\n    \"family_history\": \"No\",\n    \"work_interfere\": \"Often\",\n    \"no_employees\": \"6-25\",\n    \"remote_work\": \"No\",\n    \"tech_company\": \"Yes\",\n    \"benefits\": \"Yes\",\n    \"care_options\": \"Not sure\",\n    \"wellness_program\": \"No\",\n    \"seek_help\": \"Yes\",\n    \"anonymity\": \"Yes\",\n    \"leave\": \"Somewhat easy\",\n    \"mental_health_consequence\": \"No\",\n    \"phys_health_consequence\": \"No\",\n    \"coworkers\": \"Some of them\",\n    \"supervisor\": \"Yes\",\n    \"mental_health_interview\": \"No\",\n    \"phys_health_interview\": \"Maybe\",\n    \"mental_vs_physical\": \"Yes\",\n    \"obs_consequence\": \"No\",\n    \"comments\": null\n}",
            "data": json
            }
    
        $.ajax(settings).done(function (response) {
        console.log(response);
        }); 