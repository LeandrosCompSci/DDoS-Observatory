/* 
 * cc-common
 *
 * Alistair King, CAIDA, UC San Diego
 * corsaro-info@caida.org
 * 
 * Copyright (C) 2012 The Regents of the University of California.
 * 
 * This file is part of cc-common.
 *
 * cc-common is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * cc-common is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with cc-common.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#ifndef __IP_UTILS_H
#define __IP_UTILS_H

/** Represents a IPv4 prefix
 * e.g. 192.168.0.0/16
 */
typedef struct ip_prefix 
{
  /** The address component of the prefix */
  uint32_t addr;
  /** The length of the prefix mask */
  uint8_t masklen;
} ip_prefix_t;

/** An element in a linked list of IP prefixes */
typedef struct ip_prefix_list
{
  /** The prefix that this element represents */
  ip_prefix_t prefix;
  /** The next prefix in the list */
  struct ip_prefix_list *next;
} ip_prefix_list_t;


/** 
 * Set a bit in an IP address to a given value
 *
 * @param addr      The address to set the bit in
 * @param bitno     The bit index to set
 * @param val       The value (0 or 1) to set the bit to
 * @return the address with the corresponding bit set to the given value
 * @note MSB is bit 1, LSB is bit 32
 */
uint32_t ip_set_bit(uint32_t addr, int bitno, int val);

/** 
 * Compute netmask address given a prefix bit length
 *
 * @param masklen   The mask length to calculate the netmask address for
 * @return the network mask for the given bit length
 */
uint32_t ip_netmask(int masklen);

/**
 * Compute broadcast address given address and prefix
 *
 * @param addr      The address to calculate the broadcast address for
 * @param masklen   The mask length to apply to the address
 * @return the broadcast address for the given prefix
 */
uint32_t ip_broadcast_addr(uint32_t addr, int masklen);

/**
 * Compute network address given address and prefix
 *
 * @param addr      The address to calculate the network address for
 * @param masklen   The mask length to apply to the address
 * @return the network address for the given prefix
 */
uint32_t ip_network_addr(uint32_t addr, int masklen);

/**
 * Compute the minimal list of prefixes which this range represents
 *
 * @param lower         The lower bound of the range
 * @param upper         The upper bound of the range
 * @param[out] pfx_list A linked list of prefixes
 * @return 0 if the list is successfully built, -1 if an error occurs
 *
 * @note the pfx_list returned MUST be free'd using ip_prefix_list_free
 */
int ip_range_to_prefix(ip_prefix_t lower, ip_prefix_t upper, 
		       ip_prefix_list_t **pfx_list);

/** 
 * Free a list of prefixes as returned by ip_range_to_prefix
 *
 * @param pfx_list      The list to free
 */
void ip_prefix_list_free(ip_prefix_list_t *pfx_list);

#endif /* __IP_UTILS_H */
