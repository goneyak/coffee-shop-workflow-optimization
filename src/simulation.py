import numpy as np
from dataclasses import dataclass
from typing import Optional


@dataclass
class Order:
    """Represents a single customer order with menu and modifiers."""
    drink_type: str  # espresso, americano, flat_white, latte_capp, etc.
    requires_shots: bool
    requires_milk: bool
    t_till: float  # Service time at Till (seconds)
    t_shots: float  # Service time at Shots (seconds)
    t_milk: float  # Service time at Milk (seconds)


def lambda_of_time(t_hours, peak_profile=None):
    """
    Compute arrival rate at time t_hours.
    peak_profile: list of (start_hour, end_hour, rate) tuples, or None for constant
    Returns: arrival rate (customers/hour)
    """
    if peak_profile is None:
        return 60  # default constant rate
    
    for start, end, rate in peak_profile:
        if start <= t_hours < end:
            return rate
    
    return 60  # default fallback
    

def sample_order(menu_mix: dict, modifiers: dict, service_times_hours: dict) -> Order:
    """
    Sample an order from menu_mix with modifier probabilities.
    
    Args:
        menu_mix: dict of {drink_type: probability}
        modifiers: dict of {modifier_name: probability}
        service_times_seconds: dict of base times and extras for each stage
    
    Returns:
        Order object with calculated service times
    """
    # Sample drink type
    drinks = list(menu_mix.keys())
    probs = list(menu_mix.values())
    drink_type = np.random.choice(drinks, p=probs)
    
    # Define which drinks need shots and/or milk
    requires_shots_map = {
        'espresso': True,
        'americano': True,
        'flat_white': True,
        'latte_capp': True,
        'flavour_latte': True,
        'hot_choc': False,
        'chai': False,
        'matcha': False,
        'batch_brew': False,
        'tea': False,
        'herbal_tea': False,
        'single_origin': False,  # handled separately as pourover
    }
    
    requires_milk_map = {
        'espresso': False,
        'americano': False,
        'flat_white': True,
        'latte_capp': True,
        'flavour_latte': True,
        'hot_choc': True,
        'chai': True,
        'matcha': True,
        'batch_brew': False,
        'tea': False,
        'herbal_tea': False,
        'single_origin': False,
    }
    
    requires_shots = requires_shots_map.get(drink_type, False)
    requires_milk = requires_milk_map.get(drink_type, False)
    
    # Sample modifiers
    has_syrup = np.random.random() < modifiers.get('syrup_prob', 0.25)
    is_decaf = np.random.random() < modifiers.get('decaf_prob', 0.08)
    is_iced = np.random.random() < modifiers.get('iced_prob', 0.18)
    is_oat = np.random.random() < modifiers.get('oat_prob', 0.22)
    is_lowfat = (not is_oat) and (np.random.random() < modifiers.get('lowfat_prob', 0.10))
    is_cash = np.random.random() < modifiers.get('cash_prob', 0.20)
    wants_loyalty = np.random.random() < modifiers.get('loyalty_attempt_prob', 0.50)
    wants_upsell = np.random.random() < modifiers.get('upsell_attempt_prob', 0.40)
    is_complex = sum([is_oat, is_lowfat, is_decaf, is_iced]) > 1
    
    # Calculate Till time
    shots_cfg = service_times_seconds.get('shots', {})
    milk_cfg = service_times_seconds.get('milk', {})
    till_cfg = service_times_seconds.get('till', {})
    
    t_till = till_cfg.get('base', 12)
    if is_cash:
        t_till += till_cfg.get('cash_extra', 8)
    if wants_loyalty:
        t_till += till_cfg.get('loyalty_extra', 6)
    if wants_upsell:
        t_till += till_cfg.get('upsell_extra', 3)
    if is_complex:
        t_till += till_cfg.get('customization_extra', 4)
    
    # Calculate Shots time
    t_shots = 0.0
    if requires_shots:
        t_shots = shots_cfg.get('base_shot', 30)
        if is_decaf:
            t_shots += shots_cfg.get('decaf_extra', 10)
        else:
            # Single/double espresso logic (simplified: let's assume default is double)
            t_shots += shots_cfg.get('double_extra', 6)
    
    # Calculate Milk time
    t_milk = 0.0
    if requires_milk:
        if drink_type == 'hot_choc':
            t_milk = milk_cfg.get('hot_choc_extra', 20) + milk_cfg.get('auto_milk', 25)
        elif drink_type == 'chai':
            t_milk = milk_cfg.get('chai_extra', 15) + milk_cfg.get('auto_milk', 25)
        elif drink_type == 'matcha':
            t_milk = milk_cfg.get('matcha_extra', 25) + milk_cfg.get('auto_milk', 25)
        else:
            # latte, cappuccino, flat white, etc.
            t_milk = milk_cfg.get('auto_milk', 25)
            if is_oat:
                t_milk += milk_cfg.get('oat_extra', 15)
            elif is_lowfat:
                t_milk += milk_cfg.get('lowfat_extra', 15)
            if is_iced:
                t_milk += milk_cfg.get('iced_extra', 8)
        
        if has_syrup:
            t_milk += milk_cfg.get('syrup_extra', 2)
    
    return Order(
        drink_type=drink_type,
        requires_shots=requires_shots,
        requires_milk=requires_milk,
        t_till=t_till,
        t_shots=t_shots,
        t_milk=t_milk
    )

    """
    Compute arrival rate at time t_hours.
    peak_profile: list of (start_hour, end_hour, rate) tuples, or None for constant
    Returns: arrival rate (customers/hour)
    """
    if peak_profile is None:
        return 60  # default constant rate
    
    for start, end, rate in peak_profile:
        if start <= t_hours < end:
            return rate
    
    return 60  # default fallback

def simulate(arrival_rate, mu0, mu1, mu2, sim_time_hours, dt, seed=None, peak_profile=None, preorder_enabled=False, servers=(1,1,1), menu_config=None):
    """
    Simulate a multi-stage queueing system.
    
    Args:
        arrival_rate: average arrival rate (customers/hour)
        mu0, mu1, mu2: service rates (only used if menu_config is None)
        sim_time_hours: simulation duration
        dt: time step (hours); converted to seconds for menu-based service
        seed: random seed
        peak_profile: time-varying arrival profile
        preorder_enabled: whether to use preorder buffering
        servers: tuple (s0, s1, s2) for number of servers at each stage
        menu_config: dict with menu_mix, modifiers, service_times_seconds
                     If provided, uses job-level service times (budget-based).
                     If None, uses classic Poisson capacity.
    """
    
    if seed is not None:
        np.random.seed(seed)

    steps = int(sim_time_hours / dt)
    dt_seconds = dt * 3600  # Convert dt from hours to seconds
    
    # Queue tracking (counts for classic mode, lists of Orders for menu mode)
    if menu_config is None:
        q0 = 0  # Till
        q1 = 0  # Shots
        q2 = 0  # Milk
        use_menu_mode = False
    else:
        q0 = []  # Till queue (list of Orders)
        q1 = []  # Shots queue
        q2 = []  # Milk queue
        use_menu_mode = True
    
    preorder_q1 = [] if (preorder_enabled and use_menu_mode) else (0 if preorder_enabled else None)
    
    completed = 0
    total_queue = 0
    queue_series = []
    q0_series = []
    q1_series = []
    q2_series = []
    
    s0, s1, s2 = servers

    for step_idx in range(steps):
        t = step_idx * dt
        
        if peak_profile is not None:
            current_lambda = lambda_of_time(t, peak_profile)
        else:
            current_lambda = arrival_rate

        # ===== 1. ARRIVALS =====
        num_arrivals = np.random.poisson(current_lambda * dt)
        
        if use_menu_mode:
            for _ in range(num_arrivals):
                order = sample_order(
                    menu_config['menu_mix'],
                    menu_config['modifiers'],
                        menu_config['service_times_hours']
                )
                q0.append(order)
        else:
            q0 += num_arrivals

        # ===== 2. TILL SERVICE =====
        if use_menu_mode:
            # Budget-based service (all times in hours)
            budget = dt * s0
            while budget > 0 and len(q0) > 0:
                order = q0[0]
                if order.t_till <= budget:
                    q0.pop(0)
                    budget -= order.t_till
                    # Route to next stage based on order requirements
                    if order.requires_shots or order.requires_milk:
                        if preorder_enabled:
                            preorder_q1.append(order)
                        else:
                            q1.append(order)
                    else:
                        completed += 1
                else:
                    break
        else:
            # Classic Poisson capacity
            service0 = np.random.poisson(mu0 * dt * s0)
            served0 = min(q0, service0)
            q0 -= served0
            if preorder_enabled:
                preorder_q1 += served0
            else:
                q1 += served0

        # ===== 3. SHOTS SERVICE =====
        if use_menu_mode:
            # Budget-based service (all times in hours)
            budget = dt * s1
            # Preorder queue first (if enabled)
            if preorder_enabled and len(preorder_q1) > 0:
                while budget > 0 and len(preorder_q1) > 0:
                    order = preorder_q1[0]
                    if order.t_shots <= budget:
                        preorder_q1.pop(0)
                        budget -= order.t_shots
                        if order.requires_milk:
                            q2.append(order)
                        else:
                            completed += 1
                    else:
                        break
            # Regular queue (only orders that require shots)
            while budget > 0 and len(q1) > 0:
                order = q1[0]
                if order.t_shots <= budget:
                    q1.pop(0)
                    budget -= order.t_shots
                    if order.requires_milk:
                        q2.append(order)
                    else:
                        completed += 1
                else:
                    break
        else:
            # Classic mode
            service1 = np.random.poisson(mu1 * dt * s1)

        # ===== 4. MILK SERVICE =====
        if use_menu_mode:
            budget = dt * s2
            while budget > 0 and len(q2) > 0:
                order = q2[0]
                if order.t_milk <= budget:
                    q2.pop(0)
                    budget -= order.t_milk
                    completed += 1
                else:
                    break
        else:
            service2 = np.random.poisson(mu2 * dt * s2)
            served2 = min(q2, service2)
            q2 -= served2
            completed += served2

        # ===== METRICS COLLECTION =====
        if use_menu_mode:
            curr_total = len(q0) + len(q1) + len(q2)
            if preorder_enabled:
                curr_total += len(preorder_q1)
            total_queue += curr_total
            queue_series.append(curr_total)
            q0_series.append(len(q0))
            q1_series.append(len(q1))
            q2_series.append(len(q2))
        else:
            total_queue += (q0 + q1 + q2)
            queue_series.append(q0 + q1 + q2)
            q0_series.append(q0)
            q1_series.append(q1)
            q2_series.append(q2)

    avg_queue_length = total_queue / steps
    throughput = completed / sim_time_hours
    
    avg_q0 = np.mean(q0_series)
    avg_q1 = np.mean(q1_series)
    avg_q2 = np.mean(q2_series)
    peak_q0 = np.max(q0_series)
    peak_total = np.max(queue_series)

    return {
        "avg_queue_length": avg_queue_length,
        "throughput": throughput,
        "completed": completed,
        "queue_series": queue_series,
        "avg_q0": avg_q0,
        "avg_q1": avg_q1,
        "avg_q2": avg_q2,
        "peak_q0": peak_q0,
        "peak_total": peak_total
    }