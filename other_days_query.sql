SET HEADING OFF;
SET FEEDBACK OFF;
SET PAGESIZE 50000;
SET LINESIZE 32767;
SET COLSEP ',';
SPOOL nemo_other_days.csv;

-- Your other days SQL query here
SELECT
    abc.*,
    xyz.last_ds_delivery_dt,
    round((abc.composable_rcm_resp_received_dt - xyz.last_ds_delivery_dt) * 24 * 60) AS total_nemo_time
FROM
    (
        SELECT
            a.polnumber,
            a.corelationid,
            t.evnt_id                                    AS cdf_p1p2_to_composable_eventid,
            t.msg_updt_dt                                AS cdf_p1p2_rqst_sent_to_composable_dt,
            b.load_dt                                    AS composable_rcm_resp_received_dt,
            round((b.load_dt - t.msg_updt_dt) * 24 * 60) AS total_ca_time_mins,
            t.msg_stat
        FROM
            dwnld_hub_s01.api_msg_inpt_dtls a
            LEFT OUTER JOIN aws_kafka_s01.msg_evnt_to_hub t 
              ON t.rqst_evnt_id = a.unique_msg_id
              AND t.msg_stat != 'SKIP'
            LEFT OUTER JOIN dwnld_hub_s01.raw_cdf_event_case_metadata b 
              ON b.externalcaseid = a.unique_msg_id
              AND b.status != 'DUPLICATE'
              AND upper(b.username) = 'COMPOSABLE'
              AND upper(b.eventsubtype) = 'RESPONSE'
            LEFT OUTER JOIN dwnld_hub_s01.p8_doc                      p 
              ON p.trns_id = b.eventid
            LEFT OUTER JOIN dwnld_hub_s01.message_events              m 
              ON m.trns_id = b.eventid
        WHERE
                upper(a.servicetype) = 'RISKCLASSMODEL'
            AND upper(a.vendorid) = 'COMPOSABLE'
           -- AND a.load_dt > sysdate - 60
            AND a.load_dt >= trunc(sysdate) - 1
            AND a.load_dt < trunc(sysdate)
        ORDER BY
            a.load_dt DESC
    ) abc
    LEFT OUTER JOIN (
        SELECT
            MAX(t1.msg_updt_dt) AS last_ds_delivery_dt,
            rqst.polnumber
        FROM
            aws_kafka_s01.msg_evnt_to_hub          t1,
            dwnld_hub_s01.genius_rqmt_ordr_request rqst
        WHERE
                t1.rqst_evnt_id = rqst.msg_id
            AND rqst.msg_prvdr = 'COMPOSABLE'
            AND rqst.servicetype IN ( 'INTELRX', 'MVR', 'MIBREQUESTORDER' )
            AND t1.msg_src = 'COMPOSABLE'
        GROUP BY
            rqst.polnumber
    ) xyz ON abc.polnumber = xyz.polnumber;

SPOOL OFF;
EXIT;
