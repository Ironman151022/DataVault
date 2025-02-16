
ONTOLOGY ->
classDiagram
    %% Layer 0 - Root nodes
    class User["User (0.1)"] {
        +update_maintenance_details()
        +view_notifications()
        +view_health_status()
        +view_equipment_details()
        +respond_to_alerts()
        +wants_to_diagnose_machine()
        +follows_workflow
    }
    class iHz["iHz (0.2)"] {
        +monitors()
        +collects_data()
        +processes_data()
        +collection_interval: 5min
    }
    class BasicParameters["BasicParameters (0.3)"]{
        +check_abnormalities()
    }
    class SpectrumAnalysis["SpectrumAnalysis (0.4)"]{
        +perform_spectrum_analysis()
        spectrum_agent()
    }

    %% Layer 1
    class Machine["Machine (1.1)"] {
        +operational_state
        +health_state
        +equipment_id
        +location
    }
    class Notification["Notification (1.2)"] {
        +notification_message: string
        +is_sent: boolean[true]
        +notification_type: enum[anomaly,health,overload,started,stopped]
        +send_notification()
    }
    class MaintenanceRecord["MaintenanceRecord (1.3)"] {
        +maintenance_id
        +equipment_id
        +maintenance_type
        +maintenance_date
        +work_done
        +parts_replaced
        +technician_details
        +next_maintenance_due
    }
    class EquipmentDetailSheet["EquipmentDetailSheet (1.4)"] {
        +equipment_id
        +installation_date
        +last_maintenance_date
        +location_details
        +update_details()
    }

    %% Layer 2
    class RawData["RawData (2.1)"] {
        +current_waveform
        +timestamp
        +time_domain
        +collection_frequency: 5min
    }
    class Database["Database (2.2)"] {
        +store_maintenance_records()
        +store_notifications_records()
        +store_health_metrics()
        +update_equipment_details()
        +query_recent_data()
    }
    class MotorSpecifications["MotorSpecifications (2.3)"] {
        +motor_type
        +rated_power
        +rated_speed
        +rated_voltage
        +rated_current
        +number_of_poles
        +insulation_class
    }
    class DriveTrainComponents["DriveTrainComponents (2.4)"] {
        +coupling_type
        +gear_ratio
        +belt_type
        +pulley_sizes
    }
    class BearingDetails["BearingDetails (2.5)"] {
        +bearing_type
        +bearing_numbers
        +inner_diameter
        +outer_diameter
        +characteristic_frequencies
    }
    class LoadComponents["LoadComponents (2.6)"] {
        +load_type
        +rated_capacity
        +operating_range
    }

    %% Layer 3
    class PrimaryFeatures["PrimaryFeatures (3.1)"] {
        +i_rms
        +thd
        +kurtosis
        +fft_spectrum
        +dfft_spectrum
    }

    %% Layer 4
    class DerivedFeatures["DerivedFeatures (4.1)"] {
        +motor_speed_rpm
        +supply_frequency
        +load_percentage
        +waveform_features
        +irms_features
    }
    class BigData["BigData (4.2)"] {
        +store_derived_features()
        +store_historical_data()
        +store_spectrum_data()
    }

    %% Layer 5
    class WaveformFeatures["WaveformFeatures (5.1)"] {
        +shape_factor
        +crest_factor
        +skewness
        +kurtosis
        +mean
        +min
        +max
        +zct_std
    }
    class FrequencyFeatures["FrequencyFeatures (5.2)"] {
        +supply_freq_hz
        +supply_amplitude_db
        +shaft_positive_amplitude_db
        +shaft_negative_amplitude_db
        +shaft_frequency_hz
    }
    class AnomalyClassifier["AnomalyClassifier (5.3)"] {
        +health_status: enum[normal, watch, alarm]
        +anomaly_score: float
        +confidence_level: float
        +derived_features_values: json
        +classify_anomaly()
        +generates_derived_features_contribution()
    }
    class OperationalStatus["OperationalStatus (5.4)"] {
        +status: enum[stopped, started, running, overloaded]
        +state_changes
        +last_update_time
    }

    %% Layer 6
    class MCSAAgent["MCSAAgent (6.1)"] {
        +root_cause_analysis()
        +feature_contribution_analysis()
        +generate_mcsa_comment()
        +mcsa_comment: str
    }
    class HealthMetrics["HealthMetrics (6.2)"] {
        +health_status: enum[normal, watch, alarm]
        +mcsa_comment: enum[null, comment]
        +anomaly_score: float
        +confidence_level: float
        +HealthMetrics(List of health parameters): json
        +event_timestamp: str
    }

    %% Layer 7
    class NotificationManager["NotificationManager (7.1)"] {
        +check_notification_relevance()
        +compare_with_last_notification()
        +manage_notification_fatigue()
        +generate_notification_message()
        +send_notification()
    }

    %% Layer 8
    class NotificationRecord["NotificationRecord (8.1)"] {
        +created_on: timestamp
        +notification_message: string
        +mcsa_comment: string
        +is_notify: boolean
        +notification_type: enum[anomaly,health,overload,started,stopped]
        +health_status: enum[alarm, watch]
        +anomaly_score
    }

    %% Relationships
    Machine --> EquipmentDetailSheet : described_by
    EquipmentDetailSheet --> MotorSpecifications : contains
    EquipmentDetailSheet --> DriveTrainComponents : includes
    EquipmentDetailSheet --> BearingDetails : specifies
    EquipmentDetailSheet --> LoadComponents : defines
    iHz --> Machine : monitors
    Machine --> RawData : generates
    RawData --> PrimaryFeatures : extracted_to
    PrimaryFeatures --> DerivedFeatures : processed_to
    DerivedFeatures --> WaveformFeatures : includes
    DerivedFeatures --> FrequencyFeatures : includes
    DerivedFeatures --> AnomalyClassifier : feeds_into
    AnomalyClassifier --> MCSAAgent : triggers_if_alarm
    AnomalyClassifier --> HealthMetrics: generates_if_normal
    MCSAAgent --> HealthMetrics : generates
    DerivedFeatures --> OperationalStatus : determines
    HealthMetrics --> NotificationManager : triggers_if_alarm
    OperationalStatus --> NotificationManager : triggers
    NotificationManager --> NotificationRecord : creates
    NotificationManager ..> NotificationRecord : checks_previous
    Notification --> User: sends_to
    MaintenanceRecord --> Database : stored_in
    NotificationRecord --> Database : stored_in
    NotificationRecord --> Notification: triggers_if_is_notify_true
    HealthMetrics --> Database : stored_in
    DerivedFeatures --> BigData : stored_in
    EquipmentDetailSheet --> Database : stored_in
    PrimaryFeatures --> BigData : stores_spectrum_data
    User --> MaintenanceRecord : creates/updates
    User --> EquipmentDetailSheet : updates
    User --> Notification: views
    User --> recieved_alert : respond_to
    User --> anomaly : observed
    BasicParameters --> SpectrumAnalysis : if_any_abnormalities
    SpectrumAnalysis --> PrimaryFeatures : extracted_from 
    User --> scheduled_checkup: for_planned_inspection
    recieved_alert --> BasicParameters : targets
    anomaly --> BasicParameters : targets
    scheduled_checkup --> BasicParameters : targets
    BasicParameters --> HealthMetrics : denotes
    EquipmentDetailSheet ..> AnomalyClassifier : influences
    EquipmentDetailSheet ..> MCSAAgent : influences
    EquipmentDetailSheet ..> HealthMetrics : influences_thresholds
    EquipmentDetailSheet ..> OperationalStatus : defines_parameters
    MaintenanceRecord ..> HealthMetrics : influences_thresholds
