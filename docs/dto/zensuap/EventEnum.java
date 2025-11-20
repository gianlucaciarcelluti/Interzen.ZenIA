package it.interzen.zencommonlibrary.dto.zensuap;

/**
 * Rappresenta tutti i possibili eventi che possono verificarsi a seguito di una chiamata "notify"
 */
public enum EventEnum {
    end_by_proceeding_time_expired,
    end_by_integration_times_expired,
    end_by_submitter_cancel_requested,
    end_by_suspension_requested,
    integration_request_time_expired,
    end_by_positive_outcome,
    end_by_conformation_requested,
    end_by_negative_outcome,
    cdss_convened
}
